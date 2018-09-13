from django.db import models

class News(models.Model):
    id = models.AutoField(primary_key=True)
    news_title = models.CharField(max_length=200) 
    news_content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    def get_news(self, news_id, fields='*'):

        try:
            one_news = News.objects.get(id=news_id)
            news_info = {}
            if fields == '*':
                news_info = one_news.__dict__
            else:
                tp_name = type(fields).__name__
                if tp_name == 'list':
                    pass
                elif tp_name == 'str':
                    fields = fields.split(',')
                else:
                    return False

                for a in fields:
                    if a == '':
                        continue
                    if hasattr(one_news, a):
                        news_info[a] = one_news.__dict__[a]
        except self.DoesNotExist:
            return False

        return news_info
