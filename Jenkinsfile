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
        echo env.BRANCH_NAME
      }
    }
  }
}
