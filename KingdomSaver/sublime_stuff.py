import random
import json
import sys
bag = []
bag_sterelized = {}
class items:
	def __init__(self, name, kind, value, sell_price):
		self.name = name
		self.kind = kind
		self.value = value
		self.sell_price = sell_price
		self.quantity = 0
		self.identity = id(self)


	def add_to_bag(self, num):
		if self.name not in bag:
			bag.append(self.name)
			self.quantity = num
		else:
			self.quantity += num



	def remove_from_bag(self,num):
		if self.quantity == 0:
			return(False)
		elif self.quantity == 1:
			bag.remove(self.name)
			return(False)
		elif self.quantity > 1:
			self.quantity -= num
			if self.quantity <= 0:
				bag.remove(self.name)
				self.quantity = 0
		else:
			print("Error [1]", self.quantity)
class player:
	def __init__(self,name):
		self.max_hp = 20
		self.current_hp = 20
		self.name = name
		self.level = 1
		self.faction = None
		self.atk = 10
		self.dfn = 10
		self.coins = 0
		self.exp = 0
		self.armor_name = ""
		self.armor_value = 0
		self.weapon_name = ""
		self.weapon_value = 0
		self.location = "starting_area"
		self.bag = bag
	def level_up(self):
		self.level += 1
		self.atk += self.level
		self.dfn += self.level
		self.coins += self.level
		if self.level >= 20:
			self.max_hp += self.level
			self.current_hp += self.level
		else:
			self.max_hp += random.randint(0,self.level) + 2
			self.max_hp += random.randint(0,self.level) + 2
	def attempt_level_up(self):
		needed_exp = self.level * 20
		if self.exp >= needed_exp:
			self.exp -= needed_exp
			level_up()
		elif self.exp < needed_exp:
			print("You need {} more exp to level up!".format(needed_exp - self.exp))
	def increase_exp(self, amt):
		needed_exp = self.level * 20
		self.exp += amt
		if self.exp >= needed_exp:
			print("You are elibible to level up!")
	def show_player_info(self):
		print(self.name, "Level ", self.level)
		print("{} out of {} HP".format(self.current_hp, self.max_hp))
		print("Part of {} faction".format(self.faction))
		print(self.exp, " exp out of ", self.level*20)
		print("Weapon: {}, {} Damage".format(self.weapon_name, self.weapon_value))
		print("Armor: {}, {} Defense".format(self.armor_name, self.armor_value))
		print("Coins: {}".format(self.coins))
		print("Bag Contents:")
		for i in bag:
			print(i, "x{}".format(eval(i).quantity))
	def equipWeapon(self, wpn):
		self.weapon_name = wpn.name
		self.weapon_value = wpn.value
	def equipArmor(self, amr):
		self.armor_name = amr.name
		self.armor_value = amr.value
	def loadGame(self):
		with open("playerData.json", "r") as file:
			data = json.load(file)
			print(data)
			for i in data:
				print(i)
				loaded_name = i
				print('-------')
				self.max_hp = data[loaded_name]['max_hp']
				self.current_hp = data[loaded_name]['current_hp']
				self.level = data[loaded_name]['level']
				self.faction = data[loaded_name]['faction']
				self.atk = data[loaded_name]['atk']
				self.dfn = data[loaded_name]['dfn']
				self.coins = data[loaded_name]['coins']
				self.exp = data[loaded_name]['exp']
				self.armor_name = data[loaded_name]['armor_name']
				self.armor_value = data[loaded_name]['armor_value']
				self.weapon_name = data[loaded_name]['weapon_name']
				self.weapon_value = data[loaded_name]['weapon_value']
				self.location = data[loaded_name]['location']
				global bag
				bag = []
				for i in bag_sterelized:
					bag.append(i)
def sterelize_bag():
	bag_sterelized = {}
	for i in bag:
		if type(i) == items:
			print(i.name)
			bag_sterelized[i.name] = i.__dict__
		else:
			print(type(i))
	return(bag_sterelized)
def show_menu(called_from):
	menu_options = {"1": printBag(),
	 "2": playerinfo(),
	 "3": equipScreen(),
	 "4": fastTravel(),
	 "5": str(called_from),
	 "6": saveAndQuit()}
	print("(1) Check bag")
	print("(2) Look at my info")
	print("(3) Equip a weapon/armor")
	print("(4) Fast travel")
	print("(5) Exit")
	print("(6) Save and quit game")
	menu_choice = input(">>> ")
	try:
		exec(menu_options[menu_choice])
	except:
		exec(str(called_from))
def printBag():
	print("Bag contents: ")
	for i in bag:
		print(eval(i).name, eval(i).quantity)
def initClasses():
	global apple
	global potion
	global dagger
	global chestplate
	##ITEMS -- name, kind, value, sell_price
	apple = items("apple", "healing", 15,10)
	potion = items("potion", "healing",40,15)
	dagger = items("Dagger", "weapon", 9, 22)
	chestplate = items("chestplate", "armor", 20, 20)
initClasses()
def equipMenu(called_from):
	tempdict= {}
	index = 1
	for i in bag:
		tempdict[index] = i
		index += 1
	tempdict[index] = "Exit"
	for i in tempdict:
		if tempdict[i] != 'Exit':
			print(i, tempdict[i].name)
		else:
			print(i, tempdict[i])
	try:
		user_choice = int(input(">>>  "))
		item_selected = tempdict[user_choice]
		if item_selected.kind == "armor":
			user.equipArmor(item_selected)
			bag.remove(item_selected)
	except:
		exec(called_from)
def saveAndQuit():
	##Compiles player data into a JSON object
	userdata = {
		user.name: {
			"max_hp" : user.max_hp,
			"current_hp" : user.max_hp,
			"name" : user.name,
			"level" : user.level,
			"faction" : user.faction,
			"atk" : user.atk,
			"dfn" : user.dfn,
			"coins" : user.coins,
			"exp" : user.exp,
			"armor_name" : user.armor_name,
			"armor_value" : user.armor_value,
			"weapon_name"  : user.weapon_name,
			"weapon_value" : user.weapon_value,
			"location" : user.location,
			"bag" : sterelize_bag()
		}
	}
	with open("playerData.json", "w") as file:
		json.dump(userdata, file)
def deletesave():
	with open("playerData.json", 'w') as file:
		x = {}
		auth = random.randint(1,1000)
		print("Type {} to delete save file".format(auth))
		auth_attempt = input()
		if auth == int(auth_attempt):
			json.dump(x, file)
			print("Deleted!")
		else:
			print("Auth key was {} which was a(n)".format(auth, type(auth)))
			print("You typed {}".format(auth_attempt, type(auth)))

#GAME STARTS HERE
#GAME STARTS HERE
#GAME STARTS HERE
#GAME STARTS HERE
user = player('jake')
deletesave()
user.show_player_info()
def game_start():
	print("Long ago there was a King who ruled ofer the entire land.")
	print("He ruled for 50 years, with everyone in the populous fond of him")
	print("But one day, the 5th of may, he was assassinated.")
	print("Till")
