from django.db import models

class TicketBDManeger(models.Manager):
# this class is push models
    CustomModels=None

    def is_autors(self, user, pk) -> bool:
        q = self.vireficate_art(user, pk)
        if q == None:
            return False
        return q.autors == user

    def is_maneger(self, user, pk) -> bool:
        q = self.vireficate_art(user, pk)
        if q == None:
            return False
        return q.maneger == user

    def get_role(self, user, pk) -> str:
        """ get  3 role autor ,maneger , none"""
        if self.is_autors(user, pk):
            return "autor"
        if self.is_maneger(user, pk):
            return "maneger"
        else: 
            return "anon"
        

    def vireficate_art(self, user, pk):
        # verif using group and user
        if not isinstance(user, self.CustomModels):
            raise ValueError
        q2 = self.get(pk=pk)  # art on vert
        if user == q2.autors:
            return q2
        q = self.filter(groups__in=user.groups.all())  # list rec
        if q2 in q:
            return q2
        else:
            raise ValueError

    def get_article_user_autor(self, user):
        q = self.filter(autors=user)
        return list(q)

    def get_article_user_maneger(self, user):
        q = self.filter(maneger=user)
        return list(q)

    def get_group_article(self, user):
        gr = user.groups.all()
        q = self.filter(groups__in=gr).filter(maneger=None)
        Q = set(q) -set(self.get_article_user_autor(user)) - set(self.get_end_task(q))
        return list(Q)

    def get_end_task(self, Q):
        Q = Q.filter(status=self.model.STATUS[-1][0])
        return Q
