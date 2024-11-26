# Study Hours Estimator
Task: **Regression**

The purpose of this project is to create a machine learning model that predicts the total number of study hours a student may need to prepare for a particular topic or course. Using general features such as target exam score, sleep hours, motivation level, and access to resources, the model will predict the number of studying required and the result will be processed and categorized into categories of estimated hours(+-2). This is a regression task aimed at helping students plan their study schedules by providing time estimates that align with their individual learning needs, habits, and current circumstances.

### About the Dataset:

Sourced from: https://www.kaggle.com/datasets/lainguyn123/student-performance-factors
Provenance: The "Student Performance Factors" dataset is a synthetic dataset generated for educational and analytical purposes. The data is not sourced from any real-world institutions but is created to simulate realistic scenarios for analyzing student performance factors.

### About the project

**Package Manager:** uv: Python packaging in Rust
**Virtual Environment:** uv virtual environment
**Web Deployment:** Flask
**Container:** Docker
**Cloud Service:** AWS Beanstalk

### How to use the project

#### Clone the repository on your device
First, clone this repository by executing this prompt on the CLI:
```
git clone https://github.com/kabsmeiou/study-hours-estimator.git
```

#### Creating the environment
Create a virtual environment with:
```
pip -m venv .venv
```

Upon creating the environment, activate it with

**Windows:**
```
.venv/Scripts/activate
```
or
**Unix-based systems**
```
source .venv/bin/Activate
```

Install the dependencies by
```
pip install -r requirements
```

or you may install **uv package manager** on your system and simply run
```
uv sync
```
read the docs:https://docs.astral.sh/uv/getting-started/installation/ for details about installation.

#### Running the app
Now, make sure you have Docker installed on your system and build the project with the following command
```
docker build -t study-app .
```

Then, on your terminal, run this command:
```
docker run -it --rm -p 9696:9696 study-app
```
In case of the error ***docker: permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Head "http://%2Fvar%2Frun%2Fdocker.sock/_ping": dial unix /var/run/docker.sock: connect: permission denied.***, add *sudo* to the commands above with *docker build* and *docker run*.

You should see something like this:
![alt text](https://i.imgur.com/EbwbfFa.png)

Finally, you may access 
```
http://localhost:9696/student_form
```
and start filling out the forms to get predictions!


### Note on Cloud deployment

After successfully deploying it to cloud, I opted to not keep it running to avoid unintended costs.

Here are some of the images proving a successful app deployment on AWS Beanstalk:
![Environment Details](https://i.imgur.com/CfruF1s.png)
![Logs](https://i.imgur.com/epne76z.png)

### Video demonstration with AWS Beanstalk domain
https://github.com/user-attachments/assets/d53d4159-bc53-4385-838e-55a5b2fc6751

