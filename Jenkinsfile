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
        bat '''C:/Users/ss112148/AppData/Roaming/npm/newman run "https://www.getpostman.com/collections/283270367034f868cf40"'''
        echo env.BRANCH_NAME
      }
    }
  }
}
