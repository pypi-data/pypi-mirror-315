# IMU Drivers for Lord 3DMGX5-AHRS


# Install

```
# Install maturin 
https://www.maturin.rs/installation

# Change to correct pyenv
# ie. pyenv activate superenv

# Install drivers package
maturin develop

# Run python script using the package
python stream_imu_buff.py
```


# Develop

```
cargo build
```

Develop (compile) as python package:

```
maturin develop
```

