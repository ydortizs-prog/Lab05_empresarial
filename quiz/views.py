from django.shortcuts import render, get_object_or_404, redirect
from .models import Exam, Question, Choice
from .forms import ExamForm, QuestionForm, ChoiceForm


def exam_list(request):
    exams = Exam.objects.all().order_by('-created_at')
    return render(request, 'quiz/exam_list.html', {'exams': exams})


def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    return render(request, 'quiz/exam_detail.html', {'exam': exam, 'questions': questions})


def question_create(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Save the question first
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            
            # Save the choices with the question link
            formset = ChoiceForm(request.POST)
            if formset.is_valid():
                for form in formset.forms:
                    choice = form.save(commit=False)
                    choice.question = question
                    # Validate that only one correct answer per question
                    if choice.is_correct:
                        existing_correct = Choice.objects.filter(question=question, is_correct=True).count()
                        if existing_correct > 0:
                            raise ValueError("Sólo puede haber una opción correcta por pregunta.")
                    choice.save()
            return redirect('exam_detail', exam_id=exam.id)
    else:
        form = QuestionForm()
        formset = ChoiceForm()
    return render(request, 'quiz/question_create.html', {'form': form, 'formset': formset, 'exam': exam})