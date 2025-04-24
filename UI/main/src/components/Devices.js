import React from "react";

const Device = () => {
    return (
        <div className="container">
            <div className="card" style="width:400px">
                <img className="card-img-top" src="img_avatar1.png" alt="Card image" />
                    <div className="card-body">
                        <h4 className="card-title">Electrodes</h4>
                        <p className="card-text">Electric conductors which will pass electricity through the body.</p>
                        <a href="#" className="btn btn-primary">See details</a>
                    </div>
            </div>
            <div className="card" style="width:400px">
                <img className="card-img-top" src="img_avatar1.png" alt="Card image" />
                    <div className="card-body">
                        <h4 className="card-title">ESP32-C6</h4>
                        <p className="card-text">The ESP32-C6 is a microcontroller from Espressif Systems featuring a high-performance 
                            32-bit RISC-V processor and a low-power 32-bit RISC-V processor. It also includes Wi-Fi 6, Bluetooth 5.3, and 
                            IEEE 802.15.4 (Thread/Zigbee) connectivity, along with 30 or 22 GPIOs. 
                        </p>
                        <a href="#" className="btn btn-primary">See details</a>
                    </div>
            </div>
        </div>
    );
}
export default Device;