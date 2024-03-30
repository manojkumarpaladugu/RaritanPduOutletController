pipeline {
    agent { dockerfile true } // Use Dockerfile as the agent for the pipeline
    stages {
        stage('Build') {
            steps {
                sh './UbuntuBuild.sh'
            }
        }
    }
}