from components.models import Evaluation as EvaluationModel
class Evaluation:
    def __init__(self,request) -> None:
        self.__questions = request.POST.getlist('question[]')
        self.__choices = request.POST.getlist('choice[]')
        self.__isCorrect = request.POST.getlist('is_correct[]')
        self.__course = request.POST['course']
        self.__initChoices()
        self.__initQuestions()

    def __initChoices(self):
        self.choices_groups = [[] for i in range(len(self.__questions))]
        flag = -1
        for i in self.__isCorrect:
            self.__choices[int(i)] = self.__choices[int(i)] + " correct answer"

        for i in range(len(self.__choices)):
            if(i % 4 == 0):
                flag = flag + 1
            self.choices_groups[flag].append({"description": self.__choices[i] } )
    def __initQuestions(self):
        self.questions_groups = []
        
        for i in range(len(self.__questions)):
            self.questions_groups.append({"question": self.__questions[i], "choices": self.choices_groups[i]}) 
    
    def getEvaluation(self) -> dict:
        return {"course": self.__course, "questions": self.questions_groups}
    def getLastEvaluationBD(self) -> dict:
        queryEva = EvaluationModel.objects.last()
        return {"course": queryEva.course, "questions": queryEva.question}

    def saveEvaluation(self):
        var_eva = self.getEvaluation()
        newEva = EvaluationModel(course=var_eva['course'], question=var_eva['questions'])
        newEva.save()