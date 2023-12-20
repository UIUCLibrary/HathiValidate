import org.jenkinsci.plugins.pipeline.modeldefinition.Utils

def conditionalStage(args = [:]){
    def stageName = args['name']
    def condition = args['condition']
    def body = args['body']
    stage(stageName){
        if (condition){
            echo "Running stage ${STAGE_NAME}"
            body()
        } else {
            echo "skipping stage ${STAGE_NAME}"
            Utils.markStageSkippedForConditional(STAGE_NAME)
        }
    }

}

return [
    conditionalStage: this.&conditionalStage,
]