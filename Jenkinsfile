pipeline {
  agent any
  stages {
    stage("build") {
      when {
        expression {
          BRANCH_NAME == 'master' && GIT_COMMIT == true
        }
      }
      steps {
        echo 'building the application'
      }
    }
  }
}
