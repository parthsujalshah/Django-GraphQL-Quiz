import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Quizzes, Category, Question, Answer

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name')

class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ('id', 'title', 'category', 'quiz')

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ('id', 'title', 'quiz', 'answer')

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ('id', 'question', 'answer_text')


class Query(graphene.ObjectType):

    # all_quizzes = DjangoListField(QuizzesType) # This doesn't require resolver function
    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())

    def resolve_all_questions(root, info, id):
        return Question.objects.get(pk=id)
    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)


class CategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CategoryMutation(category=category)

class CategoryUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, id):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return CategoryUpdate(category=category)

class Mutation(graphene.ObjectType):

    add_category = CategoryMutation.Field()
    update_category = CategoryUpdate.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)