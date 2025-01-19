from DBHelper import DBHelper

db = DBHelper()

db.registerUser("waris@email.com", "abc")
db.registerUser("alberto@email.com", "abc")
db.registerUser("dayell@email.com", "abc")

db.createProfile(1, "friends", {"instagram":"waris.baris"},"")
db.createProfile(1, "networking", {"linkedin":"waris.baris"},"")
db.createProfile(2, "friends", {"instagram":"alby"},"")
db.createProfile(2, "networking", {"github":"alby"},"")
db.createProfile(3, "friends", {"discord":"nitewell"},"")
db.createProfile(3, "networking", {"github":"nitewell"},"")

db.saveProfile(1, 3)
db.saveProfile(1, 5)
db.saveProfile(2, 2)
db.saveProfile(2, 6)
db.saveProfile(3, 1)
db.saveProfile(3, 2)
db.saveProfile(3, 3)
db.saveProfile(3, 4)