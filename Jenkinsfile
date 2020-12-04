pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh '''#!/bin/bash
                docker build -t nfmstudios/project-olly:master .
                docker network create -d bridge project-olly-net
                docker run -d --network=project-olly-net -e "POSTGRES_PASSWORD=secret_password" -e "POSTGRES_USER=olly" --name project-olly-db postgres:12
                sleep 30
                '''
            }
        }
        stage('Test') {
            steps {
                sh '''#!/bin/bash
                docker run --network=project-olly-net --env-file .env.example --name project-olly nfmstudios/project-olly:master python3 manage.py test 
                '''
            }
        }
    }
    post {
        success {
            withCredentials([string(credentialsId: 'Webook_URL', variable: 'WEBHOOK_URL')]) {
                discordSend description: 'Build Success', link: 'env.BUILD_URL', result: 'SUCCESS', title: 'env.JOB_NAME', webhookURL: 'env.WEBHOOK_URL'
                }
            }
        failure {
                withCredentials([string(credentialsId: 'Webook_URL', variable: 'webhook_url')]) {
                discordSend description: 'Build Success', link: 'env.BUILD_URL', result: 'FAILURE', title: 'env.JOB_NAME', webhookURL: 'env.WEBHOOK_URL'
                }
            }
        cleanup {
            sh '''#!/bin/bash
            docker rm -f project-olly 2> /dev/null
            docker rm -f project-olly-db 2> /dev/null
            docker network rm project-olly-net 2> /dev/null
            docker rmi nfmstudios/project-olly:master 2> /dev/null 
            '''
        }
    }
}
