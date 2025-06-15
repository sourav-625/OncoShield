import React from "react";

const Device = () => {
    return (
        <div className="container">
            <h2>The devices that we intend to use for this project.</h2>

            <div className="row">
                <div className="col-md-4">
                    <div className="card">
                        <img className="card-img-top" src="/assets/battery.jpg" alt="IR Sensor" />
                        <div className="card-body">
                            <h4 className="card-title">6V battery</h4>
                        </div>
                    </div>
                </div>

                <div className="col-md-4">
                    <div className="card">
                        <img className="card-img-top" src="/assets/IR-sensor-Module-1.jpg" alt="Infrared Sensor" />
                        <div className="card-body">
                            <h4 className="card-title">Infrared Sensor</h4>
                        </div>
                    </div>
                </div>

                <div className="col-md-4">
                    <div className="card">
                        <img className="card-img-top" src="/assets/nir_sensor.jpg" alt="ESP32-C6" />
                        <div className="card-body">
                            <h4 className="card-title">NIR sensor</h4>
                        </div>
                    </div>
                </div>
            </div>
            <div className="row">
                <div className="col-md-4">
                    <div className="card">
                        <img className="card-img-top" src="/assets/ESP32.jpg" alt="IR Sensor" />
                        <div className="card-body">
                            <h4 className="card-title">ESP32</h4>
                        </div>
                    </div>
                </div>

                <div className="col-md-4">
                    <div className="card">
                        <img className="card-img-top" src="/assets/electrodes.jpg" alt="Infrared Sensor" />
                        <div className="card-body">
                            <h4 className="card-title">Electrodes</h4>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    );
}
export default Device;