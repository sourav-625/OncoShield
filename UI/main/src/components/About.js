import React from 'react';

const About = () => {
    return(
        <div className='container-fluid'>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css"/>
            <script src="https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"></script>

            <p><i>
                OncoShield is a Advanced Non-Invasive Safe and Cost-effective Multi-cancer detection System. Our primary goal behind this project 
                is to provide a cheaper, painless, safe and effective alterative to traditional cancer detection systems. It's equipments and 
                setup is not much hard nor expensive and we have even integrated a specifically trained Machine Learning Model to Diagnose and 
                predict certain possible cancers in the human body.
            </i></p>
            <br />
            <p><i>
                While our project effectively does what it claims but certain types of cancer are out of it detection scope so to know more 
                in detail about what types of possible cancers this project can detect please check the manual carefully. Also please note that 
                OncoShield currently does not posses any medical certifications or acknowledged by professional medical experts so in any case 
                of conflicts between our results and professional diagnosis, professional advice is to be followed. OncoShiels does no promise 
                a 100% accuracy or precision so please do refer to medical experts in case of any doubt.
            </i></p>
        </div>
    );
}
export default About;