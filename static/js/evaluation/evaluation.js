
let indexQuestion = 4;
function ChoiceCheckbox(){
    function simpleInput() {return document.createElement('input')} 
    
    this.formCheck = function(){
        let div = document.createElement('div')
        div.className = "form-check"
        div.append(createCheck())
        div.append(createLabel())
        return div
    }

    function createLabel(){
        let label = document.createElement('label')
        label.className = "form-check-label"
        label.htmlFor=`defaultCheck${indexQuestion}`
        label.innerText = "Respuesta Correcta"
        return label
    }
    function createCheck(){
        let input = simpleInput()
        input.type = "checkbox"
        input.className = "form-check-input"
        input.name= "is_correct[]"
        input.value = indexQuestion - 1
        input.id = `defaultCheck${indexQuestion}`
        return input
    }
    
}
function FormChoices(){
    this.index = indexQuestion
    this.numberOfChoices = 4
    
    function createInput(i){
        let input = document.createElement('input')
        input.className = "form-control"
        input.name="choice[]"
        input.type="text"
        input.placeholder=`Elección ${i}`
        return input
    }

    this.divChoice = function(){
        let div = document.createElement('div')
        div.className = "my-form__choice"
        for (let i = 0; i < this.numberOfChoices; i++) {
            const choiceCheckbox = new ChoiceCheckbox(this.index)
            indexQuestion++
            div.append(createInput(i + 1))
            div.append(choiceCheckbox.formCheck())
        }
        return div
    }  
}
function FormQuestion(){
    function createLabel(){
        let label = document.createElement('label')
        label.htmlFor = "name"
        label.className = "label-question"
        label.innerText = "Pregunta:"
        return label
    }
    function createInput(){
        let input = document.createElement('input')
        input.type = "text"
        input.name = "question[]"
        input.className = "form-control input-question"
        return input
    }
    // function createButton(){
    //     let button = document.createElement("button")
    //     button.className = "btn btn-outline-danger button-question"
    //     button.innerText = "Delete Question"
    //     button.type = "button"
    //     button.attributes="data-repeater-delete"
    //     return button
    // }
    this.divQuestion = function(){
        let div = document.createElement('div')
        div.className = "my-form__question"
        div.append(createLabel())
        div.append(createInput())
        // div.append(createButton())
        return div
    }
}
function MainQuestion(formChoices, formQuestion){
    this.formChoices = formChoices
    this.formQuestion = formQuestion
    this.divMainQuestion = function(){
        let div = document.createElement('div')
        div.className = "my-form__main-question"
        div.append(this.formQuestion.divQuestion())
        div.append(this.formChoices.divChoice())
        return div
    }

}
const init = () =>{
    const addButton = document.getElementById('add-question');
    addButton.addEventListener("click",()=>{
        const questions = document.getElementById("questions")
        const newQuestion = new FormQuestion()
        const newChoices = new FormChoices()
        questions.append(new MainQuestion(newChoices,newQuestion).divMainQuestion())
    })
}
init()