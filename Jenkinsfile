pipeline {
  agent any
  stages {
    stage("build") {
      when {
        expression {
          BRANCH_NAME == 'master'
        }
      }
      steps {
        bat '''newman run "https://www.getpostman.com/collections/283270367034f868cf40" -x -r htmlextra'''
        echo env.BRANCH_NAME
      }
    }
  }
}
