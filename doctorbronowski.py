import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users

class Worker(db.Model):
  id = db.IntegerProperty()
  firstname = db.StringProperty()

class Weekday(db.Model):
  id = db.IntegerProperty()
  name = db.StringProperty()

class Tasks(db.Model):
  worker_id = db.IntegerProperty()
  weekday_id = db.IntegerProperty()
  tasks_completed = db.IntegerProperty()


class MainPage(webapp2.RequestHandler):
    def get(self):
        template_vals = GetTaskValues()
        template = jinja_environment.get_template('/html/index.html')
        self.response.out.write(template.render(template_vals))        
        
class Spreadsheet(webapp2.RequestHandler):
    def get(self):
        template_vals = GetTaskValues()
        template = jinja_environment.get_template('/html/tasks_spreadsheet.html')
        self.response.out.write(template.render(template_vals))        

class Daily(webapp2.RequestHandler):
    def get(self):
        template_vals = GetTaskValues()
        template = jinja_environment.get_template('/html/tasks_daily.html')
        self.response.out.write(template.render(template_vals))        

class Weekly(webapp2.RequestHandler):
    def get(self):
        template_vals = GetTaskValues()
        template = jinja_environment.get_template('/html/tasks_weekly.html')
        self.response.out.write(template.render(template_vals))        

class UploadData(webapp2.RequestHandler):
    def get(self):
        PerformUploadData()
        template = jinja_environment.get_template('/html/upload.html')
        self.response.out.write(template.render())


app = webapp2.WSGIApplication([
                               ('/', MainPage),
                               ('/spreadsheet', Spreadsheet),
                               ('/daily', Daily),
                               ('/weekly', Weekly),
                               ('/uploaddata', UploadData)
                               ],
                              debug=True)
                              
                              
                              
### SUBROUTINES ###

def GetTaskValues ():
    tmpworkers  = db.GqlQuery("select * from Worker order by id")
    tmpweekdays = db.GqlQuery("select * from Weekday order by id")
    tmptasks    = db.GqlQuery("select * from Tasks order by worker_id, weekday_id")
    
    workers = ''
    for tmpworker in tmpworkers:
        workers += tmpworker.firstname + '|'
    workers = workers[:-1]
    
    weekdays = ''
    for tmpweekday in tmpweekdays:
        weekdays += tmpweekday.name + '|'
    weekdays = weekdays[:-1]
    
    tasks1 = ''
    tasks2 = ''
    tasks3 = ''
    tasks4 = ''
    tasks5 = ''
    tasks1ttl = 0
    tasks2ttl = 0
    tasks3ttl = 0
    tasks4ttl = 0
    tasks5ttl = 0
    maxval = 0
    
    for tmptask in tmptasks:
        if tmptask.worker_id == 1:
            tasks1 += str(tmptask.tasks_completed) + ','
            tasks1ttl += tmptask.tasks_completed
        elif tmptask.worker_id == 2:
            tasks2 += str(tmptask.tasks_completed) + ','
            tasks2ttl += tmptask.tasks_completed
        elif tmptask.worker_id == 3:
            tasks3 += str(tmptask.tasks_completed) + ','
            tasks3ttl += tmptask.tasks_completed
        elif tmptask.worker_id == 4:
            tasks4 += str(tmptask.tasks_completed) + ','
            tasks4ttl += tmptask.tasks_completed
        elif tmptask.worker_id == 5:
            tasks5 += str(tmptask.tasks_completed) + ','
            tasks5ttl += tmptask.tasks_completed
        if tmptask.tasks_completed > maxval:
            maxval = tmptask.tasks_completed
        
    tasks1 = tasks1[:-1]
    tasks2 = tasks2[:-1]
    tasks3 = tasks3[:-1]
    tasks4 = tasks4[:-1]
    tasks5 = tasks5[:-1]
    
    maxval = round((maxval+5) / 10) * 10
            
    template_values = {
        'rawworkers': tmpworkers,
        'rawweekdays': tmpweekdays,
        'rawtasks': tmptasks,
        'workers': workers,
        'weekdays': weekdays,
        'tasks1': tasks1,
        'tasks2': tasks2,
        'tasks3': tasks3,
        'tasks4': tasks4,
        'tasks5': tasks5,
        'tasks1ttl': tasks1ttl,
        'tasks2ttl': tasks2ttl,
        'tasks3ttl': tasks3ttl,
        'tasks4ttl': tasks4ttl,
        'tasks5ttl': tasks5ttl,
        'maxval': maxval,
        'foo': 0
    }
    
    return template_values

    
    
def PerformUploadData ():
        worker = Worker(key_name='Erine',id=1,firstname='Erine')
        worker.put()
        worker = Worker(key_name='Shea',id=2,firstname='Shea')
        worker.put()
        worker = Worker(key_name='Carly',id=3,firstname='Carly')
        worker.put()
        worker = Worker(key_name='Stu',id=4,firstname='Stu')
        worker.put()
        worker = Worker(key_name='Bernadette',id=5,firstname='Bernadette')
        worker.put()
        weekday = Weekday(key_name='Monday',id=1,name='Monday')
        weekday.put()
        weekday = Weekday(key_name='Tuesday',id=2,name='Tuesday')
        weekday.put()
        weekday = Weekday(key_name='Wednesday',id=3,name='Wednesday')
        weekday.put()
        weekday = Weekday(key_name='Thursday',id=4,name='Thursday')
        weekday.put()
        weekday = Weekday(key_name='Friday',id=5,name='Friday')
        weekday.put()
        task = Tasks(worker_id=1,weekday_id=1,tasks_completed=2)
        task.put()
        task = Tasks(worker_id=1,weekday_id=2,tasks_completed=17)
        task.put()
        task = Tasks(worker_id=1,weekday_id=3,tasks_completed=33)
        task.put()
        task = Tasks(worker_id=1,weekday_id=4,tasks_completed=44)
        task.put()
        task = Tasks(worker_id=1,weekday_id=5,tasks_completed=2)
        task.put()
        task = Tasks(worker_id=2,weekday_id=1,tasks_completed=7)
        task.put()
        task = Tasks(worker_id=2,weekday_id=2,tasks_completed=27)
        task.put()
        task = Tasks(worker_id=2,weekday_id=3,tasks_completed=9)
        task.put()
        task = Tasks(worker_id=2,weekday_id=4,tasks_completed=17)
        task.put()
        task = Tasks(worker_id=2,weekday_id=5,tasks_completed=12)
        task.put()
        task = Tasks(worker_id=3,weekday_id=1,tasks_completed=5)
        task.put()
        task = Tasks(worker_id=3,weekday_id=2,tasks_completed=12)
        task.put()
        task = Tasks(worker_id=3,weekday_id=3,tasks_completed=17)
        task.put()
        task = Tasks(worker_id=3,weekday_id=4,tasks_completed=12)
        task.put()
        task = Tasks(worker_id=3,weekday_id=5,tasks_completed=12)
        task.put()
        task = Tasks(worker_id=4,weekday_id=1,tasks_completed=8)
        task.put()
        task = Tasks(worker_id=4,weekday_id=2,tasks_completed=33)
        task.put()
        task = Tasks(worker_id=4,weekday_id=3,tasks_completed=18)
        task.put()
        task = Tasks(worker_id=4,weekday_id=4,tasks_completed=24)
        task.put()
        task = Tasks(worker_id=4,weekday_id=5,tasks_completed=15)
        task.put()
        task = Tasks(worker_id=5,weekday_id=1,tasks_completed=12)
        task.put()
        task = Tasks(worker_id=5,weekday_id=2,tasks_completed=57)
        task.put()
        task = Tasks(worker_id=5,weekday_id=3,tasks_completed=18)
        task.put()
        task = Tasks(worker_id=5,weekday_id=4,tasks_completed=49)
        task.put()
        task = Tasks(worker_id=5,weekday_id=5,tasks_completed=17)
        task.put()
