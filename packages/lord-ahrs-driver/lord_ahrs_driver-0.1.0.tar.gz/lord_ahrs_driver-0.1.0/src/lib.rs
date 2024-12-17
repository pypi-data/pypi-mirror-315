use std::{collections::HashMap, f32::consts::E, io::{Read, Seek, SeekFrom, Write}, mem::{replace, swap}, os::unix::thread, process::Output, sync::Mutex};

use crossbeam_channel::{bounded, Receiver};
use pyo3::{exceptions::PyValueError, prelude::*, types::{PyDict, PyString}};
use pyo3::conversion::IntoPyObject;
use binrw::{
    binread, binrw, binwrite, io::{self, NoSeek}, BinRead, BinWrite // trait for writing
};
use serialport::ErrorKind;
use std::time::Duration;
use binrw::io::{Cursor};
use std::fs::File;
use std::thread::spawn;
use std::time::{SystemTime, UNIX_EPOCH};


const MAGIC: &[u8] = b"ue";

#[derive(BinRead, BinWrite, Debug)]
#[brw(repr = u8)]
pub enum Descriptor {
    CommandBase = 0x01,
    Command3DM = 0x0C,
    CommandNav = 0x0D,
    CommandGNSS = 0x0E,
    CommandRTK = 0x0F,
    CommandSys = 0x7F,
    DataSensor = 0x80,
    DataGNSS = 0x81,
    DataEstimationFilter = 0x82,
    DataDisplacement = 0x90,
    DataGNSS1 = 0x91,
    DataGNSS2 = 0x92,
    DataGNSS3 = 0x93, // Can also be RTK
    DataGNSS4 = 0x94,
    DataGNSS5 = 0x95,
    DataSystem = 0xA0,
}

impl<'py> IntoPyObject<'py> for Descriptor {
    type Target = PyString; // the Python type
    type Output = Bound<'py, Self::Target>; // in most cases this will be `Bound`
    type Error = std::convert::Infallible; // the conversion error type, has to be convertable to `PyErr`

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        let s = match self {
            Descriptor::CommandBase => "CommandBase",
            Descriptor::Command3DM => "Command3DM",
            Descriptor::CommandNav => "CommandNav",
            Descriptor::CommandGNSS => "CommandGNSS",
            Descriptor::CommandRTK => "CommandRTK",
            Descriptor::CommandSys => "CommandSys",
            Descriptor::DataSensor => "DataSensor",
            Descriptor::DataGNSS => "DataGNSS",
            Descriptor::DataEstimationFilter => "DataEstimationFilter",
            Descriptor::DataDisplacement => "DataDisplacement",
            Descriptor::DataGNSS1 => "DataGNSS1",
            Descriptor::DataGNSS2 => "DataGNSS2",
            Descriptor::DataGNSS3 => "DataGNSS3",
            Descriptor::DataGNSS4 => "DataGNSS4",
            Descriptor::DataGNSS5 => "DataGNSS5",
            Descriptor::DataSystem => "DataSystem",
        };
        Ok(PyString::new(py, s))
    }
}

#[derive(BinRead, Debug)]
#[br(repr = u16)]
pub enum FilterState {
    Startup = 0x00,
    Initialization = 0x01,
    RunningValid = 0x02,
    RunningError = 0x03
}

impl<'py> IntoPyObject<'py> for FilterState {
    type Target = PyString; // the Python type
    type Output = Bound<'py, Self::Target>; // in most cases this will be `Bound`
    type Error = std::convert::Infallible; // the conversion error type, has to be convertable to `PyErr`

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        let s = match self {
            FilterState::Startup => "Startup",
            FilterState::Initialization => "Initialization",
            FilterState::RunningValid => "RunningValid",
            FilterState::RunningError => "RunningError",
        };
        Ok(PyString::new(py, s))
    }
}

#[derive(BinRead, Debug)]
#[br(repr = u16)]
pub enum DynamicsMode {
    Portable = 0x01,
    Automotive = 0x02,
    Airborne = 0x03
}

impl<'py> IntoPyObject<'py> for DynamicsMode {
    type Target = PyString; // the Python type
    type Output = Bound<'py, Self::Target>; // in most cases this will be `Bound`
    type Error = std::convert::Infallible; // the conversion error type, has to be convertable to `PyErr`

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        let s = match self {
            DynamicsMode::Portable => "Portable",
            DynamicsMode::Automotive => "Automotive",
            DynamicsMode::Airborne => "Airborne",
        };
        Ok(PyString::new(py, s))
    }
}


#[derive(BinRead, BinWrite, Debug)]
#[brw(repr = u16)]
pub enum ValidFlag {
    Invalid = 0x0000,
    Valid = 0x0001
}

impl<'py> IntoPyObject<'py> for ValidFlag {
    type Target = PyString; // the Python type
    type Output = Bound<'py, Self::Target>; // in most cases this will be `Bound`
    type Error = std::convert::Infallible; // the conversion error type, has to be convertable to `PyErr`

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        let s = match self {
            ValidFlag::Invalid => "Invalid",
            ValidFlag::Valid => "Valid",
        };
        Ok(PyString::new(py, s))
    }
}


#[derive(Debug)]
struct AHRSError {
    error: String
}

impl std::fmt::Display for AHRSError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "AHRSError: {}", self.error)
    }
}

impl std::error::Error for AHRSError {
    fn description(&self) -> &str {
        &self.error
    }
}



impl std::convert::From<AHRSError> for PyErr {
    fn from(err: AHRSError) -> PyErr {
        PyValueError::new_err(err.to_string())
    }
}

impl From<std::io::Error> for AHRSError {
    fn from(err: std::io::Error) -> Self {
        AHRSError{ error: format!("IOError: {:?}", err) }
    }   
}

impl From<serialport::Error> for AHRSError {
    fn from(err: serialport::Error) -> Self {
        AHRSError{ error: format!("SerialPortError: {:?}", err) }
    }   
}


#[derive(BinRead, BinWrite, Debug)]
#[brw(repr = u16)]
pub enum StatusFlags {
    // AttitudeNotInitialized = 0x1000,
    PosAndVelNotInitialized = 0x2000,
    IMUUnavailable = 0x0001,
    GNSS = 0x0002,
    MatrixSingularityInCalculation = 0x0008,
    PositionCovarianceHighWarning = 0x0010,
    VelocityCovarianceHighWarning = 0x0020,
    AttitudeCovarianceHighWarning = 0x0040,
    NanInSolution = 0x0080,
    GyroBiasEstimateHighWarning = 0x0100,
    AccelBiasEstimateHighWarning = 0x0200,
    GyroScaleEstimateHighWarning = 0x0400,
    AccelScaleEstimateHighWarning = 0x0800,
    MagBiasEstimateHighWarning = 0x1000, // Can also be Attitude not Initialized if during startup/initialization
    HardIronOffsetHighWarning = 0x4000,
    SoftIronCorrectionHighWarning = 0x8000,
}

// 0x0001 – IMU unavailable
// 0x0002 – GNSS (GNSS versions only)
// 0x0008 – Matrix singularity in calculation
// 0x0010 – Position covariance high warning*
// 0x0020 – Velocity covariance high warning*
// 0x0040 – Attitude covariance high warning*
// 0x0080 – NAN in solution
// 0x0100 – Gyro bias estimate high warning
// 0x0200 – Accel bias estimate high warning
// 0x0400 – Gyro scale factor estimate high warning
// 0x0800 – Accel scale factor estimate high warning
// 0x1000 – Mag bias estimate high warning
// 0x4000 – Hard Iron offset estimate high warning
// 0x8000 - Soft iron correction estimate high warning

impl<'py> IntoPyObject<'py> for StatusFlags {
    type Target = PyString; // the Python type
    type Output = Bound<'py, Self::Target>; // in most cases this will be `Bound`
    type Error = std::convert::Infallible; // the conversion error type, has to be convertable to `PyErr`

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        let s = match self {
            StatusFlags::PosAndVelNotInitialized => "PosAndVelNotInitialized",
            StatusFlags::IMUUnavailable => "IMUUnavailable",
            StatusFlags::GNSS => "GNSS",
            StatusFlags::MatrixSingularityInCalculation => "MatrixSingularityInCalculation",
            StatusFlags::PositionCovarianceHighWarning => "PositionCovarianceHighWarning",
            StatusFlags::VelocityCovarianceHighWarning => "VelocityCovarianceHighWarning",
            StatusFlags::AttitudeCovarianceHighWarning => "AttitudeCovarianceHighWarning",
            StatusFlags::NanInSolution => "NanInSolution",
            StatusFlags::GyroBiasEstimateHighWarning => "GyroBiasEstimateHighWarning",
            StatusFlags::AccelBiasEstimateHighWarning => "AccelBiasEstimateHighWarning",
            StatusFlags::GyroScaleEstimateHighWarning => "GyroScaleEstimateHighWarning",
            StatusFlags::AccelScaleEstimateHighWarning => "AccelScaleEstimateHighWarning",
            StatusFlags::MagBiasEstimateHighWarning => "MagBiasEstimateHighWarning",
            StatusFlags::HardIronOffsetHighWarning => "HardIronOffsetHighWarning",
            StatusFlags::SoftIronCorrectionHighWarning => "SoftIronCorrectionHighWarning",

        };
        Ok(PyString::new(py, s))
    }
}


struct ForwardOnlySeek<T> {
    inner: T,
}

impl<T> ForwardOnlySeek<T>
where
    T: Read,
{
    fn new(inner: T) -> Self {
        ForwardOnlySeek { inner }
    }

}

impl<T> Read for ForwardOnlySeek<T>
where
    T: Read,
{
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        self.inner.read(buf)
    }
}

// Seek implementation that doesn't require the inner type to implement Seek
impl<T> std::io::Seek for ForwardOnlySeek<T>
where
    T: Read,
{
    fn seek(&mut self, pos: std::io::SeekFrom) -> io::Result<u64> {
        match pos {
            std::io::SeekFrom::Start(offset) => {
                let mut offset = offset;
                if offset > 0 {
                    // Consume bytes to move the position forward
                    let mut buffer = vec![0; 1024];
                    while offset > 0 {
                        let bytes_to_consume = std::cmp::min(buffer.len() as u64, offset);
                        self.inner.read_exact(&mut buffer[..bytes_to_consume as usize])?;
                        offset -= bytes_to_consume;
                    }
                }
                else if offset == 0 {
                    // Do nothing
                }
                else {
                    println!("Cannot seek to a negative position, {:?}", pos);
                    return Err(io::Error::new(
                        io::ErrorKind::InvalidInput,
                        "Cannot seek to a negative position",
                    ));
                }
                
                Ok(offset)
            },
            std::io::SeekFrom::Current(offset) => {

                if offset >= 0 {
                    self.seek(std::io::SeekFrom::Start(offset as u64))?;
                } else {
                    return Err(io::Error::new(
                        io::ErrorKind::InvalidInput,
                        "Cannot seek to a negative position",
                    ));
                }
                
                Ok(offset as u64)
            },
            std::io::SeekFrom::End(_) => {
                Err(io::Error::new(
                    io::ErrorKind::Other,
                    "Seeking from End is not supported in forward-only mode",
                ))
            },
        }
    }
}

// write
impl <T: Write> Write for ForwardOnlySeek<T> {
    fn write(&mut self, buf: &[u8]) -> io::Result<usize> {
        self.inner.write(buf)
    }

    fn flush(&mut self) -> io::Result<()> {
        self.inner.flush()
    }
}



// Fletcher-16 checksum
struct Checksum<T> {
    inner: T,
    checksum1: u8,
    checksum2: u8,
}

impl<T> Checksum<T> {
    fn new(inner: T) -> Self {
        Self {
            inner,
            checksum1: 0,
            checksum2: 0,
        }
    }

    fn with_magic(inner: T) -> Self {
        Self {
            inner,
            checksum1: 0xDA,
            checksum2: 0x4F,
        }
    }

    fn check(&self) -> u16 {
        // checksum = ((u16) checksum_byte1 << 8) + (u16) checksum_byte2;
        ((self.checksum1 as u16) << 8) + (self.checksum2 as u16)
    }
}

impl<T: Read> Read for Checksum<T> {
    fn read(&mut self, buf: &mut [u8]) -> std::io::Result<usize> {
        let size = self.inner.read(buf)?;
        for byte in buf.iter().take(size) {
            // print hex what is being read
            self.checksum1 = self.checksum1.wrapping_add(*byte);
            self.checksum2 = self.checksum2.wrapping_add(self.checksum1);
        }
        Ok(size)
    }
}

impl<T: Seek> Seek for Checksum<T> {
    fn seek(&mut self, pos: SeekFrom) -> std::io::Result<u64> {
        let p = self.inner.seek(pos)?;
        Ok(p)
    }
}

impl<T: Write> Write for Checksum<T> {
    fn write(&mut self, buf: &[u8]) -> std::io::Result<usize> {
        let size = self.inner.write(buf)?;
        for byte in buf.iter().take(size) {
            self.checksum1 = self.checksum1.wrapping_add(*byte);
            self.checksum2 = self.checksum2.wrapping_add(self.checksum1);
        }
        Ok(size)
    }

    fn flush(&mut self) -> std::io::Result<()> {
        self.inner.flush()
    }
}

#[binrw]
#[derive(Debug)]
#[brw(big, magic = b"ue", stream = r, map_stream = Checksum::with_magic)]
pub struct MipPacket {
    descriptor: Descriptor,
    #[bw(try_calc(u8::try_from(bytes.len())))]
    payload_length: u8,
    #[br(count = payload_length)]
    bytes: Vec<u8>,
    // #[br(seek_before = SeekFrom::Start(0))]
    // #[br(calc(r.check()))]
    // calculated_checksum: u16,
    #[bw(calc(r.check()))]
    #[br(assert(checksum != r.check(), "bad checksum: {:x?} != {:x?}", checksum, r.check()))]
    checksum: u16,
}



#[derive(BinRead, Debug, IntoPyObject)]
pub enum SensorReading {
    #[br(magic = b"\x04")]
    ScaledAccVector { x: f32, y: f32, z: f32 },
    #[br(magic = b"\x05")]
    ScaledGyroVector { x: f32, y: f32, z: f32 },
    #[br(magic = b"\x06")]
    ScaledMageVector { x: f32, y: f32, z: f32 },
    #[br(magic = b"\x07")]
    DeltaThetaVector { x: f32, y: f32, z: f32 },
    #[br(magic = b"\x08")]
    DeltaVelocityVector { x: f32, y: f32, z: f32 },
    #[br(magic = b"\x17")]
    ScaledAmbientPressure { ambient_pressure: f32 },
    #[br(magic = b"\x09")]
    CFOrientationMatrix { 
        m11: f32, m12: f32, m13: f32,
        m21: f32, m22: f32, m23: f32,
        m31: f32, m32: f32, m33: f32,
     },
    #[br(magic = b"\x0A")]
    CFQuaternion { x: f32, y: f32, z: f32, w: f32 },
    #[br(magic = b"\x0C")]
    CFEulerAngles { roll: f32, pitch: f32, yaw: f32 },
    #[br(magic = b"\x10")]
    CFStabilizedNorthVector { x: f32, y: f32, z: f32 },
    #[br(magic = b"\x11")]
    CFStabilizedUpVector { x: f32, y: f32, z: f32 },
    #[br(magic = b"\x12")]
    GPSCorrelationTimestamp { gps_time_of_week: f64, gps_week: u16, timestamp_flags: u16 },
}
impl SensorReading {
    fn type_name(&self) -> String {
        match self {
            SensorReading::ScaledAccVector { .. } => "ScaledAccVector",
            SensorReading::ScaledGyroVector { .. } => "ScaledGyroVector",
            SensorReading::ScaledMageVector { .. } => "ScaledMageVector",
            SensorReading::DeltaThetaVector { .. } => "DeltaThetaVector",
            SensorReading::DeltaVelocityVector { .. } => "DeltaVelocityVector",
            SensorReading::ScaledAmbientPressure { .. } => "ScaledAmbientPressure",
            SensorReading::CFOrientationMatrix { .. } => "CFOrientationMatrix",
            SensorReading::CFQuaternion { .. } => "CFQuaternion",
            SensorReading::CFEulerAngles { .. } => "CFEulerAngles",
            SensorReading::CFStabilizedNorthVector { .. } => "CFStabilizedNorthVector",
            SensorReading::CFStabilizedUpVector { .. } => "CFStabilizedUpVector",
            SensorReading::GPSCorrelationTimestamp { .. } => "GPSCorrelationTimestamp",
        }.to_string()
    }
}


#[derive(BinRead, Debug, IntoPyObject)]
pub enum EstimateReading {
    #[br(magic = b"\x10")]
    FilterStatus { filter_state: u16, dynamics_mode: u16, status_flags: u16 },

    #[br(magic = b"\x11")]
    GPSTimestamp { time_of_week: f64, week: u16, valid_flags: ValidFlag },

    #[br(magic = b"\x03")]
    OrientationQuaternion { x: f32, y: f32, z: f32, w: f32, valid: ValidFlag },

    #[br(magic = b"\x05")]
    OrientationEuler { roll: f32, pitch: f32, yaw: f32, valid: ValidFlag },

    #[br(magic = b"\x0A")]
    AttitudeUncertaintyEuler { roll: f32, pitch: f32, yaw: f32, valid: ValidFlag },

    #[br(magic = b"\x12")]
    AttitudeUncertaintyQuaternion { x: f32, y: f32, z: f32, w: f32, valid: ValidFlag },

    #[br(magic = b"\x04")]
    OrientationMatrix { 
        m11: f32, m12: f32, m13: f32,
        m21: f32, m22: f32, m23: f32,
        m31: f32, m32: f32, m33: f32,
        valid: ValidFlag
     },
     #[br(magic = b"\x0E")]
     CompensatedAngularRate { x: f32, y: f32, z: f32, valid: ValidFlag },

     #[br(magic = b"\x06")]
     GyroBias { x: f32, y: f32, z: f32, valid: ValidFlag },

     #[br(magic = b"\x0B")]
     GyroBiasUncertainty { x: f32, y: f32, z: f32, valid: ValidFlag },

     #[br(magic = b"\x1C")]
     CompensatedAcceleration { x: f32, y: f32, z: f32, valid: ValidFlag },

     #[br(magic = b"\x0D")]
     LinearAcceleration { x: f32, y: f32, z: f32, valid: ValidFlag },

     #[br(magic = b"\x21")]
     PressureAltitude { pressure_altitude: f32, valid: ValidFlag },

     #[br(magic = b"\x13")]
     GravityVector { x: f32, y: f32, z: f32, valid: ValidFlag },

     #[br(magic = b"\x0F")]
     WGS84LocalGravityMagnitude { gravity_magnitude: f32, valid: ValidFlag },
}

impl EstimateReading {
    fn type_name(&self) -> String {
        match self {
            EstimateReading::FilterStatus { .. } => "FilterStatus",
            EstimateReading::GPSTimestamp { .. } => "GPSTimestamp",
            EstimateReading::OrientationQuaternion { .. } => "OrientationQuaternion",
            EstimateReading::OrientationEuler { .. } => "OrientationEuler",
            EstimateReading::AttitudeUncertaintyEuler { .. } => "AttitudeUncertaintyEuler",
            EstimateReading::AttitudeUncertaintyQuaternion { .. } => "AttitudeUncertaintyQuaternion",
            EstimateReading::OrientationMatrix { .. } => "OrientationMatrix",
            EstimateReading::CompensatedAngularRate { .. } => "CompensatedAngularRate",
            EstimateReading::GyroBias { .. } => "GyroBias",
            EstimateReading::GyroBiasUncertainty { .. } => "GyroBiasUncertainty",
            EstimateReading::CompensatedAcceleration { .. } => "CompensatedAcceleration",
            EstimateReading::LinearAcceleration { .. } => "LinearAcceleration",
            EstimateReading::PressureAltitude { .. } => "PressureAltitude",
            EstimateReading::GravityVector { .. } => "GravityVector",
            EstimateReading::WGS84LocalGravityMagnitude { .. } => "WGS84LocalGravityMagnitude",
        }.to_string()
    }
}



#[derive(Debug, IntoPyObject)]
pub enum ReadingOrString {
    #[pyo3(transparent)]
    Reading(Reading),
    #[pyo3(transparent)]
    String(String),
}
impl From<String> for ReadingOrString {
    fn from(s: String) -> Self {
        ReadingOrString::String(s)
    }
}
impl From<Reading> for ReadingOrString {
    fn from(r: Reading) -> Self {
        ReadingOrString::Reading(r)
    }
}


#[derive(Debug, IntoPyObject)]
pub enum Reading {
    #[pyo3(transparent)]
    Sensor(SensorReading),
    #[pyo3(transparent)]
    Estimate(EstimateReading),
}
impl Reading {
    fn type_name(&self) -> String {
        match self {
            Reading::Sensor(reading) => reading.type_name(),
            Reading::Estimate(reading) => reading.type_name(),
        }
    }
    fn reading_type_name(&self) -> String {
        match self {
            Reading::Sensor(reading) => "sensor",
            Reading::Estimate(reading) => "estimate",
        }.to_string()
    }
}


impl MipPacket {
    pub fn to_sensor_readings(self) -> Vec<Reading> {
        self.to_sensor_readings_with_options(false, false)
    }
    pub fn to_sensor_readings_with_verbosity(self, verbose: bool) -> Vec<Reading> {
        self.to_sensor_readings_with_options(verbose, false)
    }
    pub fn to_sensor_readings_with_options(self, verbose: bool, panic_on_error: bool) -> Vec<Reading> {
        let mut readings = Vec::new();

        // Go through the whole bytes and split them into sensor readings
        // There is always first byte that tells how many bytes are in the reading
        // and then the actual reading which can be parsed using the SensorReading struct
        // when all bytes are read, the next reading starts with the first byte again

        let mut i = 0;
        // println!("Buffer length: {}, Data: {:02x?}", self.bytes.len(), self.bytes);
        loop {
            let mut reading_length = (self.bytes[i] as usize).saturating_sub(1);
            // maximum is minimum of the bytes buffer length and the reading length
            let end = std::cmp::min(i+reading_length+1, self.bytes.len());
            let mut data = self.bytes[i+1..end].to_vec();
            // i += 1;
            // 
            // println!("Reading length: {} / {}, data: {:02x?}", reading_length, data.len(), data);
            let mut reader = Cursor::new(data);
            match self.descriptor {
                Descriptor::DataSensor => {
                    match SensorReading::read_be(&mut reader) {
                        Ok(reading) => readings.push(Reading::Sensor(reading)),
                        Err(e) => {
                            if verbose {
                                eprintln!("Error parsing sensor reading: {}", e);
                            }
                            if panic_on_error {
                                panic!("Error parsing sensor reading: {}", e);
                            }
                        },
                    }
                },
                Descriptor::DataEstimationFilter => {
                    match EstimateReading::read_be(&mut reader) {
                        Ok(reading) => readings.push(Reading::Estimate(reading)),
                        Err(e) => {
                            if verbose {
                                eprintln!("Error parsing estimate reading: {}", e);
                            }
                            if panic_on_error {
                                panic!("Error parsing estimate reading: {}", e);
                            }
                        },
                    }
                },
                _ => {
                    if verbose {
                        eprintln!("Unknown descriptor: {:?}", self.descriptor);
                    }
                },
                
            };
            // println!("Read: {:?}", readings);
            // println!("Data: {:?}/{:?}", i+reading_length, self.bytes.len());
            if i + reading_length+1 >= self.bytes.len() {
                break;
            }
            i = i+reading_length+1;
        }

        readings
    }

    pub fn ping() -> Self {
        MipPacket {
            descriptor: Descriptor::CommandBase,
            bytes: vec![0x02, 0x01],
        }
    }

    pub fn set_to_idle() -> Self {
        MipPacket {
            descriptor: Descriptor::CommandBase,
            bytes: vec![0x02, 0x02],
        }
    }
    
    pub fn set_to_resume() -> Self {
        MipPacket {
            descriptor: Descriptor::CommandBase,
            bytes: vec![0x02, 0x06],
        }
    }
    
    pub fn get_device_information() -> Self {
        MipPacket {
            descriptor: Descriptor::CommandBase,
            bytes: vec![0x02, 0x03],
        }
    }

    pub fn reset_to_factory_settings() -> Self {
        MipPacket {
            descriptor: Descriptor::Command3DM,
            bytes: vec![0x03, 0x30, 0x05],
        }
    }
    pub fn save_as_startup_settings() -> Self {
        MipPacket {
            descriptor: Descriptor::Command3DM,
            bytes: vec![0x03, 0x30, 0x03],
        }
    }

    pub fn enable_imu_stream() -> Self {
        // Does not actually yet do that, only enables either imu or then estimates
        MipPacket {
            descriptor: Descriptor::Command3DM,
                                         // 1 = IMU, 3 = Estimates
            bytes: vec![0x05, 0x11, 0x01, 0x1, 0x1],
        }
    }
    pub fn disable_imu_stream() -> Self {
        // Does not actually yet do that, only enables either imu or then estimates
        MipPacket {
            descriptor: Descriptor::Command3DM,
                                         // 1 = IMU, 3 = Estimates
            bytes: vec![0x05, 0x11, 0x01, 0x1, 0x0],
        }
    }

    pub fn enable_estimate_stream() -> Self {
        // Does not actually yet do that, only enables either imu or then estimates
        MipPacket {
            descriptor: Descriptor::Command3DM,
                                         // 1 = IMU, 3 = Estimates
            bytes: vec![0x05, 0x11, 0x01, 0x3, 0x1],
        }
    }
    pub fn disable_estimate_stream() -> Self {
        // Does not actually yet do that, only enables either imu or then estimates
        MipPacket {
            descriptor: Descriptor::Command3DM,
                                         // 1 = IMU, 3 = Estimates
            bytes: vec![0x05, 0x11, 0x01, 0x3, 0x0],
        }
    }
    pub fn poll_estimate() -> Self {
        // Does not actually yet do that, only enables either imu or then estimates
        MipPacket {
            descriptor: Descriptor::Command3DM,
            bytes: vec![0x0A, 0x03, 0x01, 0x02, 0x1, 0x00, 0x00, 0x02, 0x00, 0x00],
        }
    }

    
    
}



enum PortState {
    Configuration(Box<dyn serialport::SerialPort>),
    Streaming(ForwardOnlySeek<Box<dyn serialport::SerialPort>>),
    StreamingFile(ForwardOnlySeek<File>),
    None
}

struct  Port {
    port: PortState,
}

impl Port {
    pub fn default() -> Self {
        Self {
            port: PortState::None,
        }
    }
    pub fn open(serial_device: &str, baud_rate: u32) -> Result<Self, AHRSError> {
        let port = serialport::new(serial_device, baud_rate)
        .timeout(Duration::from_millis(100))
        .open()?;

        Ok(Self {
            port: PortState::Configuration(port),
        })
    }

    pub fn open_file(filename: &str) -> Result<Self, AHRSError> {
        let file = std::fs::File::open(filename)?;
        let port = ForwardOnlySeek::new(file);
        Ok(Self {
            port: PortState::StreamingFile(port),
        })
    }

    pub fn configure(&mut self) {
        match &mut self.port {
            PortState::Configuration(p) => {
                let mut cursor = ForwardOnlySeek::new(p);
                MipPacket::set_to_idle().write(&mut cursor).unwrap();
                MipPacket::disable_imu_stream().write(&mut cursor).unwrap();
                MipPacket::disable_estimate_stream().write(&mut cursor).unwrap();

            },
            PortState::Streaming(_) => {
                eprintln!("Port already streaming");
            },
            PortState::StreamingFile(_) => {
                eprintln!("Cannot configure file stream");
            },
            PortState::None => {
                eprintln!("Port not configured");
            }
        }
    }

    pub fn start_stream(&mut self) {
        match replace(&mut self.port, PortState::None) {
            PortState::Configuration(p) => {
                let cursor = ForwardOnlySeek::new(p);
                self.port =  PortState::Streaming(cursor);
            },
            PortState::Streaming(_) => {
                eprintln!("Port already streaming");
            },
            PortState::StreamingFile(_) => {
                eprintln!("Cannot configure file stream");
            },
            PortState::None => {
                eprintln!("Port not configured");
            }
        }
    }

    pub fn read_packet(&mut self) -> Result<Vec<Reading>, AHRSError> {
        match &mut self.port {
            PortState::Configuration(_) => {
                Err(serialport::Error::new(ErrorKind::InvalidInput, "Port not streaming").into())
            },
            PortState::None => {
                Err(serialport::Error::new(ErrorKind::InvalidInput, "Port not streaming").into())
            },
            PortState::Streaming(s) => {
                match MipPacket::read_be(s) {
                    Ok(packet) => {
                        // println!("Parsed packet: {:?}", packet.descriptor);
                        let reading = packet.to_sensor_readings();
                        // println!("Sensor reading: {:?}", reading);
                        Ok(reading)
                    }
                    Err(binrw::Error::Io(e)) => {
                        // End of file
                        eprintln!("IOERR: {}", e);
                        Err(e.into())
                    }
                    Err(e) => {
                        eprintln!("Error parsing packet: {:?}", e);
                        // If parsing fails, skip one byte and try again
                        // s.seek(SeekFrom::Current(1))?;
                        // check if we are at the end of the file
                        s.seek(SeekFrom::Current(1))?;
                        Ok(vec![])
                    }
                }
            },
            PortState::StreamingFile(s) => {
                match MipPacket::read_be(s) {
                    Ok(packet) => {
                        println!("Parsed packet: {:?}", packet.descriptor);
                        let reading = packet.to_sensor_readings();
                        // println!("Sensor reading: {:?}", reading);
                        Ok(reading)
                    }
                    Err(binrw::Error::Io(e)) => {
                        // End of file
                        eprintln!("IOERR: {}", e);
                        Err(e.into())
                    }
                    Err(e) => {
                        // eprintln!("Error parsing packet: {:?}", e);
                        // If parsing fails, skip one byte and try again
                        // s.seek(SeekFrom::Current(1))?;
                        s.seek_relative(1)?;
                        // check if we are at the end of the file
                        Ok(vec![])
                    }
                }
            }
        }
    }

    
}



#[pyclass]
struct AHRSClient {
    port: Mutex<Port>,
}


fn type_of<T>(_: &T) -> String {
    format!("{}", std::any::type_name::<T>())
}

#[pymethods]
impl AHRSClient {

    #[new]
    pub fn new() -> Self {
        AHRSClient {
            port: Mutex::new(Port::default()),
        }
    }

    pub fn open(&mut self, serial_device: String, baud_rate: u32) -> Result<(), AHRSError> {
        self.port = Mutex::new(Port::open(&serial_device, baud_rate)?);
        Ok(())
    }

    pub fn open_file(&mut self, filename: String) -> Result<(), AHRSError> {
        self.port =  Mutex::new(Port::open_file(&filename)?);
        Ok(())
    }

    pub fn configure(&mut self) {
        let port = self.port.get_mut().unwrap();
        (*port).configure();
    }

    pub fn start_stream(&mut self) {
        let port = self.port.get_mut().unwrap();
        (*port).start_stream();
    }

    
    pub fn read(&mut self) -> HashMap<String, ReadingOrString> {
        if let Ok(r) = self.read_packet() {
            AHRSClient::process_readings(r)
        } else {
            HashMap::new()
        }
    }
    pub fn read_packet(&mut self) -> Result<Vec<Reading>, AHRSError> {
        if let Ok(port) = self.port.get_mut() {
            return (*port).read_packet()
        }
        Ok(vec![])
    }
}

impl AHRSClient {
    pub fn process_readings(readings: Vec<Reading>) -> HashMap<String, ReadingOrString> {
        // Process readings
        let mut imu_data = HashMap::new();
        for reading in readings {
            imu_data.insert("type".to_string(), reading.reading_type_name().into());
            imu_data.insert(reading.type_name(), reading.into());
        }
        imu_data
    }

}

#[pyclass]
struct BufferedAHRSClient {
    t: std::thread::JoinHandle<()>,
    receiver: Receiver<(u64, HashMap<String, ReadingOrString>)>,
}

#[pymethods]
impl BufferedAHRSClient {

    #[new]
    pub fn new(serial_device: String, baud_rate: u32, buffer_size: usize, verbose: bool) -> Self {
        let (sender, receive) = bounded(buffer_size);

        let t = std::thread::spawn(move || {
            let mut port = Port::open(&serial_device, baud_rate).expect("Failed to open port");
            let verbose = verbose;
            port.start_stream();
            loop {
                match port.read_packet() {
                    Ok(reading) => {
                        let hm = AHRSClient::process_readings(reading);
                        let start = SystemTime::now();
                        let since_the_epoch = start
                            .duration_since(UNIX_EPOCH)
                            .expect("Time went backwards");
                        let in_ms = since_the_epoch.as_secs() * 1000 + since_the_epoch.subsec_nanos() as u64 / 1_000_000;
                        sender.send((in_ms, hm)).expect("Failed to send reading");
                    }
                    Err(e) => {
                        if verbose {
                            eprintln!("Error parsing packet: {:?}", e);
                        }
                    }
                }
            }
        });

        BufferedAHRSClient {
            t: t,
            receiver: receive,
        }
    }

    
    pub fn take(&mut self) -> Vec<(u64, HashMap<String, ReadingOrString>)> {
        let mut readings = Vec::new();
        while let Ok(r) = self.receiver.try_recv() {
            readings.push(r);
        }
        readings
    }
}


fn parse_serial_stream(serial_device: &str, baud_rate: u32) -> Result<(), AHRSError> {
    let mut client = AHRSClient::new();
    client.open(serial_device.to_string(), baud_rate)?;
    // let mut client = AHRSClient::open(serial_device.to_string(), baud_rate)?;
    client.start_stream();

    loop {
        match client.read_packet() {
            Ok(reading) => {
                let hm = AHRSClient::process_readings(reading);
                println!("Sensor reading: {:?}", hm);
            }
            Err(e) => {
                eprintln!("Error parsing packet: {:?}", e);
                // If parsing fails, skip one byte and try again
                // reader.seek(SeekFrom::Current(1))?;
                // check if we are at the end of the file
            }
        }

    }
    Ok(())
}

fn parse_file_stream(filename: &str) -> Result<(), AHRSError> {
    let mut client = AHRSClient::new();
    client.open_file(filename.to_string())?;

    loop {
        match client.read_packet() {
            Ok(reading) => {
                let hm = AHRSClient::process_readings(reading);
                println!("Sensor reading: {:?}", hm);
            }
            Err(e) => {
                eprintln!("Error parsing packet PARSEFS: {:?}", e);
                // If parsing fails, skip one byte and try again
                // reader.seek(SeekFrom::Current(1))?;
                break;
                // check if we are at the end of the file
            }
        }

    }
    Ok(())
}

fn parse_data_stream_from_file(filename: &str) -> Result<(),AHRSError> {
    let file = std::fs::File::open(filename)?;
    let mut reader = std::io::BufReader::new(file);
    // let mut buffer = Vec::new();
    // reader.read_to_end(&mut buffer)?;

    // let mut cursor = Cursor::new(&buffer);
    loop {
        match MipPacket::read_be(&mut reader) {
            Ok(packet) => {
                // println!("Parsed packet: {:?}", packet);
                let reading = packet.to_sensor_readings();
                println!("{:?}", reading);
                
            }
            Err(binrw::Error::Io(e)) => {
                // End of file
                eprintln!("End of file: {}", e);
                break;
            }
            Err(e) => {
                eprintln!("Error parsing packet from file: {:?}", e);
                // If parsing fails, skip one byte and try again
                break;
                // reader.take(1);
                // check if we are at the end of the file
            }
        }

    }
    // process_stream(&mut reader)?;
    Ok(())
}

#[pyfunction]
fn parse_data_stream_py(filename: &str) -> PyResult<()> {
    match parse_data_stream_from_file(filename) {
        Ok(_) => Ok(()),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyOSError, _>(format!("{}", e))),
    }
}

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn lord_ahrs_driver(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse_data_stream_py, m)?)?;
    m.add_class::<AHRSClient>()?;
    m.add_class::<BufferedAHRSClient>()?;
    Ok(())
}

// tests
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sum_as_string() {
        assert_eq!(sum_as_string(1, 2).unwrap(), "3");
    }

    #[test]
    fn test_parse_data_stream() {

        parse_file_stream("download.dat").unwrap();
        
        // parse_serial_stream("/dev/tty.usbserial-ALBGb121474", 115200).unwrap();
        // assert_eq!(parse_data_stream("dump3.txt").unwrap(), ());
    }



    #[test]
    fn test_create_packet_idle() {
        let packet = MipPacket::set_to_idle();
        let mut writer = Cursor::new(Vec::new());
        packet.write(&mut writer).unwrap();
        println!("idle: {:02x?}", writer.into_inner());
    }
    #[test]
    fn test_create_packet_resume() {
        let packet = MipPacket::set_to_resume();
        let mut writer = Cursor::new(Vec::new());
        packet.write(&mut writer).unwrap();
        println!("resume: {:02x?}", writer.into_inner());
    }

    #[test]
    fn test_create_packet_devinfo() {
        let packet = MipPacket::get_device_information();
        let mut writer = Cursor::new(Vec::new());
        packet.write(&mut writer).unwrap();
        println!("devinfo: {:02x?}", writer.into_inner());
    }
    #[test]
    fn test_create_packet_enable_all() {
        let packet = MipPacket::enable_imu_stream();
        let mut writer = Cursor::new(Vec::new());
        packet.write(&mut writer).unwrap();
        println!("enable all streams: {:02x?}", writer.into_inner());
    }
    
    #[test]
    fn test_create_packet_reset_to_fac() {
        let packet = MipPacket::reset_to_factory_settings();
        let mut writer = Cursor::new(Vec::new());
        packet.write(&mut writer).unwrap();
        println!("reset to factory: {:02x?}", writer.into_inner());
    }
}