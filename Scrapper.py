import logging
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import json
from mongodb import mongodbconnection

# setting up logging file
logging.basicConfig(filename = "flask_logs.log", format = '%(asctime)s %(message)s', filemode = 'w', level = logging.DEBUG)

# Function to scrap all course title from iNeuron
def all_course():
    try:
        ineuron_url = 'https://ineuron.ai/courses/'
        uClient = uReq(ineuron_url)
        ineuron_page = uClient.read()
        uClient.close()
        ineuron_html = bs(ineuron_page, 'html.parser')
        course_data = json.loads(ineuron_html.find('script', {'id': '__NEXT_DATA__'}).get_text())
        all_courses = course_data['props']['pageProps']['initialState']['init']['courses']
        course_namelist = list(all_courses.keys())
        return course_namelist
    except:
        logging.error('Error while reading course data from all_courses()')

# Function to scrap one course details from iNeuron
def get_course(coursename):
    ineuron_url = 'https://ineuron.ai/courses/'
    uClient = uReq(ineuron_url + str(coursename).replace(" ","-"))
    course_page = uClient.read()
    uClient.close()
    ineuron_html = bs(course_page, 'html.parser')
    courseData = json.loads(ineuron_html.find('script', {"id": "__NEXT_DATA__"}).get_text())
    logging.info('Course Data saved in JSON format')
    all_dict = {}
    try:
        try:
            all_data = courseData["props"]["pageProps"]
        except:
            all_data = 'No Page'
        
        try:
            page_data = all_data['data']
        except:
            page_data = 'No data'

        try:
            detailed_data = page_data['details']
        except:
            detailed_data = 'No details'

        try:
            meta_data = page_data['meta']
        except:
            meta_data = 'No meta data'  

        try:
            curriculum_data = meta_data['curriculum']
        except:
            curriculum_data = 'No curriculum data'

        try:
            overview_data = meta_data['overview']
        except:
            overview_data = 'No overview data'

        # Building course dictionary
        try:
            price = detailed_data['priceing']['IN']
        except:
            price = 'NULL'

        try:
            course_name = page_data['title']
        except:
            course_name = 'Name NA'

        try:
            description = detailed_data['description']
        except:
            description = 'NULL'

        try:
            language = overview_data['language']
        except:
            language = 'NULL'

        try:
            req = overview_data['requirements']
        except:
            req = 'NULL'
        
        try:
            learn = overview_data['learn']
        except:
            learn = 'NULL'

        curriculum = []

        try:
            for i in curriculum_data:
                curriculum.append(curriculum_data[i]['title'])
            
            # Saving all the data in dict format
            all_dict = {'Course_title': course_name, 'Description': description, 'Language': language, 'Pricing': price, 'Curriculum_data': curriculum, 'Learn': learn, 'Requirements': req}
            logging.info('dictionary is created')
        except:
            curriculum.append('NULL')
        
        return all_dict

    except:
        logging.error('Error in Scrapping data at get_course()')


# Function to get the course data and ssave it in mongodb
def scrap_all():
    #mongodb m odule to do mongodb operations
    dbcon = mongodbconnection(username = 'mongdb', password = 'mongodb')
    db_collection = dbcon.getCollection('iNeuron_ReviewScrapper', 'course_collection')
    try:
        if dbcon.isCollectionPresent('iNeuron_ReviewScrapper','course_collection'):
            pass
        else:
            final_list = []
            lsit_courses = all_course()
            for i in lsit_courses:
                print(i)
                final_list.append(get_course(i))
            db_collection.insert_many(final_list)

    except Exception as e:
        logging.error('Error in DB insertion', e)