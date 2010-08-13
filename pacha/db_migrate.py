import confparser
import database

repos = confparser.Parse('/opt/pacha/conf/.repos')
for repo in repos.text_read():
    db = database.Worker()
    db.insert(path=repo)

