
##### Recommendation Services Setup
# git clone git@github.gatech.edu:kjeyabalan3/TheRecipator.git
1) cd TheRecipator
npm install --legacy-peer-deps 


2)pip install scikit-learn
  pip install flask
  pip install flask_cors
  pip install python-louvain
  pip install networkx

3)cd services
  recommendation_model_updated.py ----> Model
  recommendation_services_updated.py---> Web Server
  test_recommendation_services.py -- Test 

4) install pm2 
Python Flask Run using pm2

  GNU nano 5.4                                  ecosystem.config.js                                      M     
module.exports = {
  apps: [{
    name: 'recommendation_services',
    script: 'recommendation_services_updated.py',
    interpreter: '/usr/local/bin/python3.9',
    interpreter_args: '-u',
    cwd: '/home/karthi_jeyabalan/TheRecipator/services'
  }]
}
pm2 start /home/karthi_jeyabalan/TheRecipator/services/recommendation_services_updated.py --name "recommendation_services" --interpreter "/usr/local/bin/python3.9" --interpreter-args "-u"


-- npm run pm2
pm2 start npm --name "myapp" --cwd "/home/karthi_jeyabalan/TheRecipator" -- start


npm install react
npm install react-bootstrap
npm install axios
npm install @bumaga/tabs