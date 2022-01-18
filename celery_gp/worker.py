import schedule, time

from gptask import GeoprocessTask
from ..core.arcgis import controller
from ..app import celery_app

SGP = GeoprocessTask('https://cscfjina.cfjcs.net/server/rest/services/cerebro_gp/BufferPolygon', 'BufferPolygon')
SCH =  schedule
activity = None

def job():    
    SGP.runTask(activity.params) 


@celery_app.task(acks_late=True)
def geoprocess_schedule():
    print "Starting Celery worker"
    activity = controller.read({id : 1})
    SCH.every().day.at(activity.schedule).do(job)    
    celeryrunning = True

    while celeryrunning:
        activity = controller.read({id : 1})
        celeryrunning = activity.status
        SCH.run_pending()
        time.sleep(20)
    print "Stoped Celery worker"
    return True