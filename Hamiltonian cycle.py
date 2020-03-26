import pickle
import pygame
import time
import sys
import random
def auto_fill(point):
	for each in point_dic[point.pos].neighbors:
		if point_dic[each.pos].line_count!=2:
			av_nebor=[]
			av_nebor_count=0
			for each2 in each.neighbors:
				if point_dic[each2.pos].line_count!=2 and (each.pos,each2.pos) not in line_map:
					av_nebor.append(each2)
					av_nebor_count+=1
			if av_nebor_count+point_dic[each.pos].line_count<2:
				print('fail ',each2.pos)
				return 'fail'
			if av_nebor_count+point_dic[each.pos].line_count==2:
				for each3 in av_nebor:
					return point_dic[each.pos].connect(point_dic[each3.pos])
	return					
line_map=[]
class point:
	def __init__(self,pos1,pos2):
		self.pos1=pos1
		self.pos2=pos2
		self.pos=(pos1,pos2)
		self.line_count=0
		self.neighbors=[]
	def connect(self,point2):
		print(self.pos,' connect ',point2.pos)
		line_map.append((self.pos,point2.pos))
		line_map.append((point2.pos,self.pos))
		point_dic[self.pos].line_count+=1
		point_dic[point2.pos].line_count+=1
		draw(line_map)
		if auto_fill(point_dic[self.pos])=='fail' or auto_fill(point_dic[point2.pos])=='fail':
			return 'fail'
		return
point_dic={}
point_count=0
data_stack=[]
current=0
def save():
	data_stack.append(pickle.dumps((point_dic,line_map,current)))
def load():
	global point_dic,line_map,current
	point_dic,line_map,current=pickle.loads(data_stack[-1])
	del data_stack[-1]
start=0
def find():
	global current
	lab1=0
	av_list=[]
	if point_dic[current.pos].line_count==2:
		L=[]
		T=[]
		T2=[]
		T.append(start)
		L.append(start)
		while 1:
			if len(T)==0:
				break
			T2.clear()
			for each in T:
				for each2 in each.neighbors:
					if each2 not in L and (each.pos,each2.pos) in line_map:
						L.append(each2)
						if point_dic[each2.pos].line_count==1:
							av_list.append(each2)
						T2.append(each2)
			T=T2.copy()
		if len(av_list)==0:
			if len(L)<w*h-len(wall_lis):
				print('fail')
				return 'fail'
			else:
				print('done')
				return 'done'
	if len(av_list)==0:
		av_list.append(current)
	lili=av_list.copy()
	for E in lili:
		if len(lili)>=2:
			print('chose ',E.pos,' as current')
		current=E
		for each in current.neighbors:
			if point_dic[each.pos].line_count!=2 and (current.pos,each.pos) not in line_map:
				save()
				V0=current.connect(each)
				if V0!='fail':
					current=each
					Va=find()
					if Va=='done':
						return 'done'
				load()
h=0
w=0
wall_lis=[]
def load_file(file_name):
	global start
	global point_count
	global h,w
	with open(file_name, "r") as f:
		h,w=f.readline().split()
		h=int(h)
		w=int(w)
		lines=f.readlines()
		point_count=0
		for i in range(h):
			for j in range(w):
				if int(lines[i][j])==0:
					a_point=point(i,j)
					point_count+=1
					if i-1>=0:
						if point_dic[(i-1,j)]!=0:
							point_dic[(i-1,j)].neighbors.append(a_point)
							a_point.neighbors.append(point_dic[(i-1,j)])
					if j-1>=0:
						if point_dic[(i,j-1)]!=0:
							point_dic[(i,j-1)].neighbors.append(a_point)
							a_point.neighbors.append(point_dic[(i,j-1)])				
					point_dic[(i,j)]=a_point
				else:
					point_dic[(i,j)]=0
					wall_lis.append((i,j))
	lab=0
	for i in range(h):
		for j in range(w):
			if point_dic[(i,j)]!=0:
				start=point_dic[(i,j)]
				lab=1
				break
		if lab==1:
			break
def draw_lines(screen):
	for i in range(1,h):
		pygame.draw.aaline(screen, WHITE,(i*cube_height,0),(i*cube_height,screen_size[1]),5)
	for i in range(1,w):
		pygame.draw.aaline(screen, WHITE,(0,i*cube_width),(screen_size[0],i*cube_width),5)
def draw_snack(screen,body):
	lab=0
	for each in body:
		sp=[]
		if each[0][0]+each[0][1]<each[1][0]+each[1][1]:
			sp=((each[0][1]+0.25)*cube_height,(each[0][0]+0.25)*cube_width)
		else:
			sp=((each[1][1]+0.25)*cube_height,(each[1][0]+0.25)*cube_width)
		if each[1][0]==each[0][0]:
			
			wi=cube_width*1.5
			hi=cube_height/2
		else:
			wi=cube_width/2
			hi=cube_height*1.5
		pygame.draw.rect(screen,BLACK,[sp[0],sp[1],wi,hi],0)
def draw_walls(screen):
	for each in wall_lis:
		pygame.draw.rect(screen,[255,255,255],[(each[1])*cube_width,(each[0])*cube_height,cube_width,cube_height],0)
def draw(body):
	screen.fill(GREY)
	draw_lines(screen)
	if food_pos!=(-1,-1):
		pygame.draw.rect(screen,RED,[int((food_pos[1]+0.25)*cube_width),int((food_pos[0]+0.25)*cube_height),cube_width/2,cube_height/2],0)
	draw_walls(screen)
	draw_snack(screen,body)
	clock.tick(FPS)
	pygame.display.flip()
	#time.sleep(0.5)	
GREY=(111,111,111)
WHITE=(255,255,255)
RED=(255,0,0)
BLUE=(0,0,255)
BLACK=(0,0,0)
screen_size=(600,600)
cube_height=0
cube_width=0
food_pos=(-1,-1)
def rand_food():
	global food_pos
	av_li=[]
	for each in point_dic.keys():
		if each not in wall_lis:
			labb=0
			for each2 in body:
				if each==each2[0] or each==each2[1]:
					labb=1
					break
			if labb==0:
				av_li.append(each)
	if len(av_li)==0:
		food_pos=(-1,-1)
		return
	food_pos=random.choice(av_li)
body=[]		
if __name__ == "__main__":
	load_file("map.txt")
	cube_height=screen_size[0]/h
	cube_width=screen_size[1]/w
	current=start
	pygame.init()
	screen = pygame.display.set_mode(screen_size, 0, 32)
	pygame.display.set_caption("snack")
	FPS=30
	clock = pygame.time.Clock()
	find()
	rand_food()
	head=point_dic[(0,1)]
	body.append(((0,0),(0,1)))
	while 1:
		for each in head.neighbors:
			if (each.pos,head.pos) not in body and (head.pos,each.pos) not in body and (each.pos,head.pos) in line_map:
				body.append((each.pos,head.pos))
				head=each
				if head.pos!=food_pos:
					del body[0]
				else:
					rand_food()
		draw(body)
