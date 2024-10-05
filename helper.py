import firebase_admin
from firebase_admin import credentials,db



ref=db.reference('Students')


data={
    '234567':{
    'name': 'Robert Downey Jr',
    'major': 'Acting',
    'total_attendance': 6,
    'standing': 6,
    'year': 4,
    'last_attendance_time': '2024-10-04 12:30:00'
    },
    '321654':{
        'name': 'Indian Guy',
        'major': 'CSE',
        'total_attendance': 8,
        'standing': 8,
        'year': 3,
        'last_attendance_time': '2024-10-05 10:45:00'
    },
    '435423':{
        'name': 'Elon Musk',
        'major': 'IOT',
        'total_attendance': 5,
        'standing': 4,
        'year': 2,
        'last_attendance_time': '2024-10-04 15:20:00'
    },
    '852741':{
        'name': 'Emily Blunt',
        'major': 'Acting',
        'total_attendance': 7,
        'standing': 7,
        'year': 5,
        'last_attendance_time': '2024-10-03 14:50:00'
    },
    '963852':{
        'name': 'Elon',
        'major': 'Sports',
        'total_attendance': 9,
        'standing': 9,
        'year': 4,
        'last_attendance_time': '2024-10-05 08:15:00'
    },
    '987654':{
        'name': 'Eminem',
        'major': 'Music',
        'total_attendance': 10,
        'standing': 10,
        'year': 1,
        'last_attendance_time': '2024-10-05 09:05:00'
    }

}

for key,value in data.items():
    ref.child(key).set(value)