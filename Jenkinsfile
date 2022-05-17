pipeline {
  agent any
  stages {
    stage("build") {
      when {
        expression {
          BRANCH_NAME == 'postman-api' && GIT_COMMIT == true
        }
      }
      steps {
        echo 'building the application'
      }
    }
  }
}
