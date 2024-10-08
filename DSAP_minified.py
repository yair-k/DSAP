BC='Please enter a valid integer.'
BB='Please enter a positive integer.'
BA='Nail Count'
B9='How many nails do you want to use?'
B8='correct'
B7='Exit to Main Menu'
B6='chat_window_opened'
B5='Reset Canvas'
B4='Continue'
B3='current_hint'
B2='timestamp'
B1='Send to AI'
B0='Clear Canvas'
A_='String Color'
Az='Choose String Color'
Ay='Nail Color'
Ax='Choose Nail Color'
Aw='Nail Size:'
Av='Your Drawing Prompt'
Au='Settings'
At='WM_DELETE_WINDOW'
As='400x200'
Ar='Player'
Aq='1024x768'
Ap=TypeError
Ao=Exception
Ab='word'
Aa='You have placed all nails.'
AZ='Limit Reached'
AY='guess_time'
AX='message'
AW='400x300'
AV='guesses'
AU='guess'
AT='lobby/users'
AS='audio'
AR=range
AQ=sorted
AH='Invalid Input'
AG='normal'
AF='Digital String Art'
AE='guessing'
AD='game_result'
AC='Total Cost: $0.00'
AB='content'
A8='hints'
A7='guess_attempts'
A6='drawing_started_at'
A5='drawing'
A4='Error'
A3=ValueError
z='end'
y='hint_level'
x='prompt'
u='disabled'
r='drawer'
q='nail_color'
p='background'
o=''
n='string_color'
m=len
l='guesser'
k='string_thickness'
j='ended'
h=False
g='nail_size'
f='bold'
b='both'
V='left'
U='state'
T='resolution'
S='x'
Q=True
H='Monaco'
G=int
F=None
import turtle as K,tkinter as R,tkinter.ttk as J
from tkinter import messagebox as L,colorchooser as A0,simpledialog
import customtkinter as B,time as e,random as Ac,uuid as AI,firebase_admin as BD
from firebase_admin import credentials as BE,db as N
from ttkthemes import ThemedTk as Ad
import webbrowser as Ae,openai as AJ
from dotenv import load_dotenv as BF
import os
BF()
AJ.api_key=os.getenv('OPENAI_API_KEY')
BG=BE.Certificate('nails-36418-firebase-adminsdk-cmi75-307c4a5b03.json')
BD.initialize_app(BG,{'databaseURL':'https://nails-36418-default-rtdb.firebaseio.com/'})
I={T:Aq,p:'#359e56',AS:Q}
W={q:'black',g:10}
X={n:'white',k:3}
D=[]
M=0
O=0
Y=str(AI.uuid4())
v=Ar
AK=F
w=F
i=h
A=F
C=F
E=F
c=F
Z=F
P=F
d=F
a=h
def s():
	A=B.CTk();A.title('DTAP v1.0 | By: Yair K.');D=500;E=350;F=A.winfo_screenwidth();I=A.winfo_screenheight();J=G(I/2-E/2);K=G(F/2-D/2);A.geometry(f"{D}x{E}+{K}+{J}");C=B.CTkFrame(A,corner_radius=10);C.pack(expand=Q,fill=b,padx=20,pady=20);L=B.CTkLabel(C,text='Digital String Art Platform',font=(H,26,f));L.pack(pady=30)
	def M():
		A=B.CTkToplevel();A.title('Single Player Mode');A.geometry(As);B.CTkLabel(A,text='Choose Mode:',font=(H,16)).pack(pady=10)
		def C():A.destroy();BU()
		def D():A.destroy();BH()
		E=B.CTkButton(A,text='Free Draw',command=C);E.pack(pady=10);F=B.CTkButton(A,text='Vs AI',command=D);F.pack(pady=10)
		def G():A.destroy();s()
		A.protocol(At,G)
	N=B.CTkButton(C,text='Single Player Game',font=(H,18),command=lambda:[A.destroy(),M()]);N.pack(pady=10);O=B.CTkButton(C,text='Multiplayer Game',font=(H,18),command=lambda:[A.destroy(),BJ()]);O.pack(pady=10);P=B.CTkButton(C,text=Au,font=(H,18),command=BW);P.pack(pady=10);R=B.CTkButton(C,text='Info',font=(H,18),command=BX);R.pack(pady=10);Ag();A.mainloop()
def Af(prompt):
	try:A=AJ.ChatCompletion.create(model='gpt-4',messages=[{'role':'user',AB:f"Based on this description of a string art drawing: '{prompt}', what do you think the player is drawing?"}]);L.showinfo("AI's Guess",A.choices[0].message[AB].strip())
	except Ao as B:L.showerror(A4,f"An error occurred: {str(B)}")
def BH():
	Q='Digital String Art - Vs AI Mode';global A,C,D,M,O,E,A9;A1();A9=Ai();L.showinfo(Av,f"Draw the following: {A9}");AN()
	if not C or not C._root:C=K.Screen()
	else:
		try:C.reset()
		except K.Terminator:C=K.Screen()
	C.setup(width=G(I[T].split(S)[0]),height=G(I[T].split(S)[1]));C.bgcolor(I[p]);C.title(Q);A=K.Turtle();A.speed(0);A.hideturtle();E=B.CTk();E.title(Q);U,i=map(G,I[T].split(S));E.geometry(f"{U}x200");F=B.CTkFrame(E,corner_radius=10);F.pack(fill=b,padx=20,pady=10);B.CTkLabel(F,text=Aw,font=(H,12)).grid(row=0,column=0,padx=5,pady=5);N=R.IntVar(value=W[g]);V=B.CTkEntry(F,textvariable=N,width=50);V.grid(row=0,column=1,padx=5,pady=5)
	def Y():
		A=A0.askcolor(title=Ax)
		if A:W[q]=A[1]
	Z=B.CTkButton(F,text=Ay,command=Y);Z.grid(row=0,column=2,padx=5,pady=5)
	def a():
		A=A0.askcolor(title=Az)
		if A:X[n]=A[1]
	c=B.CTkButton(F,text=A_,command=a);c.grid(row=1,column=2,padx=5,pady=5);J=B.CTkLabel(F,text=AC);J.grid(row=1,column=0,padx=5,pady=5)
	def d():
		if C:C.clear()
		J.configure(text=AC)
	e=B.CTkButton(F,text=B0,command=d);e.grid(row=0,column=3,padx=5,pady=5);f=B.CTkButton(F,text=B1,command=lambda:Af(A9));f.grid(row=1,column=3,padx=5,pady=5);h=B.CTkButton(F,text='Back to Main Menu',command=lambda:[A1(),s()]);h.grid(row=0,column=5,rowspan=2,padx=10,pady=5)
	def P():
		try:W[g]=G(N.get())
		except A3:W[g]=10
		E.after(500,P)
	P();C.onscreenclick(lambda x,y:Am(x,y,J));E.mainloop()
def BZ(prompt):
	try:A=AJ.ChatCompletion.create(model='gpt-4',messages=[{'role':'user',AB:f"Based on this description of a string art drawing: '{prompt}', what do you think the player is drawing?"}]);return A.choices[0].message[AB].strip()
	except Ao as B:return f"Error: {str(B)}"
def BI():
	global Y,v;Y=str(AI.uuid4());A=B.CTkInputDialog(text='Enter your name:',title='User Name').get_input()
	if A:v=A
	else:v=Ar
def BJ():BI();BK()
def BK():
	d='pending';c='from';a='online';T='declined';S='accepted';P='name';K='game_session';J='invitation';C='status';global Y,v,AK;f={P:v,C:a,J:F,K:F,B2:e.time()};D=N.reference(AT);D.child(Y).set(f);A=B.CTk();A.title('Multiplayer Lobby');V=500;W=450;g=A.winfo_screenwidth();h=A.winfo_screenheight();i=G(h/2-W/2);j=G(g/2-V/2);A.geometry(f"{V}x{W}+{j}+{i}");E=B.CTkFrame(A,corner_radius=10);E.pack(expand=Q,fill=b,padx=20,pady=20);B.CTkLabel(E,text='Connected Players',font=(H,20)).pack(pady=10);I=R.Listbox(E,height=5,font=(H,14));I.pack(pady=10);AK=R.StringVar();M=B.CTkLabel(E,text=o,font=(H,14));M.pack(pady=10)
	def X():
		I.delete(0,R.END);A=D.get()
		if A:
			for(B,E)in A.items():
				if B!=Y and E.get(C)==a:I.insert(R.END,f"{E[P]} ({B})")
		else:I.insert(R.END,'No other players online')
	k=B.CTkButton(E,text='Refresh',command=X);k.pack(pady=10)
	def m():
		A=I.curselection()
		if A:E=I.get(A[0]);B=E.split('(')[-1].strip(')');AK.set(B);D.child(B).child(J).set({c:Y,C:d});M.configure(text='Invitation sent. Waiting for response...');O()
		else:L.showwarning('No Selection','Please select a player to invite.')
	n=B.CTkButton(E,text='Send Invitation',command=m);n.pack(pady=10)
	def O():
		E=D.child(Y).child(J);B=E.get()
		if B:
			if B.get(C)==S:F=B.get(K);A.after(0,lambda:[A.destroy(),Ah(F)])
			elif B.get(C)==T:L.showinfo('Invitation Declined','The player declined your invitation.');E.delete();M.configure(text=o)
			else:A.after(1000,O)
		else:A.after(1000,O)
	def Z():
		G=D.child(Y).child(J);B=G.get()
		if B and B.get(C)==d:
			E=B.get(c);M=D.child(E).child(P).get()
			def H():
				I='in-game';O=L.askyesno('Game Invitation',f"{M} has invited you to play. Accept?")
				if O:B=str(AI.uuid4());H=[E,Y];Ac.shuffle(H);P=H[0];Q=H[1];R=N.reference(f"games/{B}");V={r:P,l:Q,U:'waiting_for_prompt',x:F,A5:F,AU:F,AD:F,A6:F,y:0,B3:o,A7:0,AV:{},A8:{}};R.set(V);D.child(Y).update({K:B,C:I});D.child(E).update({K:B,C:I});G.update({C:S,K:B});D.child(E).child(J).update({C:S,K:B});A.after(0,lambda:[A.destroy(),Ah(B)])
				else:G.update({C:T});D.child(E).child(J).update({C:T})
			A.after(0,H)
		else:A.after(1000,Z)
	Z()
	def p():D.child(Y).delete();A.destroy()
	A.protocol(At,p);Ag();X();A.mainloop()
def Ag():
	A=N.reference(AT);B=A.get();C=e.time()
	if B:
		for(D,E)in B.items():
			F=E.get(B2,0)
			if C-F>300:A.child(D).delete()
def Ah(game_session_id):
	F=game_session_id;global Y,v;G=N.reference(f"games/{F}");D=G.get()
	if not D:L.showerror(A4,'Game session not found.');return
	if Y==D[r]:C=r
	elif Y==D[l]:C=l
	else:L.showerror(A4,'You are not part of this game.');return
	E=f"You are the {C}.\n"
	if C==r:E+="You will receive a prompt to draw. Place the nails and create your string art.\n\nOnce you are ready, click 'Send Drawing' to send it to the guesser.\n"
	else:E+='Wait for the drawer to create their string art.\n\nOnce the drawing is ready, you can start guessing.\n'
	A=B.CTk();A.title('Game Instructions');A.geometry(AW);B.CTkLabel(A,text=E,font=(H,14),wraplength=380).pack(pady=20)
	def I():A.destroy();BL(F,C)
	J=B.CTkButton(A,text=B4,command=I);J.pack(pady=10);A.mainloop()
def BL(game_session_id,player_role):
	B=player_role;A=game_session_id;global Y;D=N.reference(f"games/{A}")
	if B==r:C=Ai();D.update({x:C,U:A5,A6:e.time(),y:0,B3:o,A8:{}});BM(A,C)
	elif B==l:Aj(A)
def Ai():A=['House','Tree','Car','Cat','Dog','Sun','Flower','Boat','Bird','Fish','Bicycle','Ice Cream','Apple','Star','Cloud','Moon','Pencil','Cake','Hat','Balloon','Guitar','Robot','Cupcake','Elephant','Lion','Train','Heart','Spider','Kite','Castle','Snowman','Pumpkin','Turtle','Rainbow','Shark','Octopus','Ladybug','Scissors','Key','Musical Note','Drum','Coffee Cup','Book','Sunglasses','Telephone','Candle','Worm','Teddy Bear','Fire','Grass','Butterfly','Mushroom','Cactus','Anchor','Ice Cube','Sailboat','Laptop','Camera','Soccer Ball','Baseball Bat','Skateboard','Glasses','Map','Treasure Chest','Crab','Pineapple','Snowflake','Candy','Zebra','Penguin','Dolphin','Frog','Rocket','Alien','Grapes','Corn','Donut','Hot Air Balloon','Yacht','Whale'];return Ac.choice(A)
def BM(game_session_id,prompt):
	global Y,O,w;A=B.CTk();A.title(Av);A.geometry('300x150');B.CTkLabel(A,text=f"Your prompt is: {prompt}",font=(H,16)).pack(pady=20)
	def C():A.destroy();BS();AA(is_multiplayer=Q,is_drawing=Q,game_session_id=game_session_id);B=e.time()
	D=B.CTkButton(A,text=B4,command=C);D.pack(pady=10);A.mainloop()
def Aj(game_session_id):
	A=game_session_id;global Z;D=N.reference(f"games/{A}");Z=B.CTk();Z.title('Waiting for Drawing');Z.geometry(As);E=B.CTkLabel(Z,text='Player is drawing...',font=(H,16));E.pack(pady=50)
	def C():
		if not Z.winfo_exists():return
		B=D.get()
		if B.get(U)==AE:Z.destroy();AA(is_multiplayer=Q,is_drawing=h,game_session_id=A)
		elif B.get(U)==j:Z.destroy();L.showinfo('Game Ended','The drawer has left the game.');A2()
		elif Z.winfo_exists():Z.after(1000,C)
	Z.after(0,C);Z.mainloop()
def AA(is_multiplayer,is_drawing,game_session_id=F):
	k='Digital String Art - In-Game Taskbar';W='running';R=is_multiplayer;P=is_drawing;F=game_session_id;global A,C,D,M,O,w;global i,E,c,a;D=[];M=0;i=h;a=h
	if not C or not C._root:C=K.Screen()
	else:
		try:C.reset()
		except K.Terminator:C=K.Screen()
	C.setup(width=G(I[T].split(S)[0]),height=G(I[T].split(S)[1]));C.bgcolor(I[p]);C.title(AF);A=K.Turtle();A.speed(0);A.hideturtle()
	if R and(P or not P):
		if not c or not c.winfo_exists():c=B.CTk();c.title(k)
		Z,n=map(G,I[T].split(S));c.geometry(f"{Z}x150");J=c
	else:
		if not E or not E.winfo_exists():E=B.CTk();E.title(k)
		Z,n=map(G,I[T].split(S));E.geometry(f"{Z}x150");J=E
	for d in J.winfo_children():d.destroy()
	X=B.CTkFrame(J,corner_radius=10);X.pack(fill=b,padx=20,pady=10);f=B.CTkLabel(X,text='Time: 120',font=(H,16));f.pack(side=V,padx=10)
	if R and P:A3=N.reference(f"games/{F}");A7=A3.get();A9=A7.get(x,o);AB=B.CTkLabel(X,text=f"Prompt: {A9}",font=(H,16));AB.pack(side=V,padx=10);AC=B.CTkButton(X,text=B5,font=(H,16),command=lambda:BN(R,P,F));AC.pack(side=V,padx=10);AG=B.CTkButton(X,text='Send Drawing',font=(H,16),command=lambda:AL(R,P,F));AG.pack(side=V,padx=10);AH=B.CTkButton(X,text='Edit Drawing',font=(H,16),command=lambda:BO(R,P,F));AH.pack(side=V,padx=10)
	AI=B.CTkButton(X,text='Exit Game',font=(H,16),command=lambda:BY(F,R));AI.pack(side='right',padx=10);Y={W:Q}
	def q():
		if not Y[W]:return
		global a
		if a:return
		if R:
			B=N.reference(f"games/{F}");A=B.get()
			if not A:return
			C=G(e.time()-A.get(A6,e.time()));I=max(0,120-C);f.configure(text=f"Time: {I} sec")
			if A.get(U)==j:Y[W]=h;J.after(0,lambda:t(F,r if P else l));return
			if A.get(U)==AE:
				if P:0
				elif C>=45 and A.get(y)==0:D=A.get(x,o);E=f"The word has {m(D)} letters.";B.update({y:1});H=B.child(A8);H.push({AX:E})
				elif C>=90 and A.get(y)==1:D=A.get(x,o);E=f"The word starts with '{D[0]}' and ends with '{D[-1]}'.";B.update({y:2});H=B.child(A8);H.push({AX:E})
				elif C>=120 and A.get(U)!=j:B.update({U:j,AD:'Time Up',AY:e.time()});Y[W]=h;J.after(0,lambda:t(F,l));return
			J.after(1000,q)
		else:0
	q()
	if R and P:
		C.onscreenclick(lambda x,y:AM(x,y,R,P,F))
		def u():
			if not Y[W]:return
			global a
			if a:return
			B=N.reference(f"games/{F}");A=B.get()
			if not A:return
			if A.get(U)==j:Y[W]=h;J.after(0,lambda:t(F,r))
			elif A.get(U)==AE:
				if not hasattr(AA,B6):Ak(F);AA.chat_window_opened=Q
				else:0
			else:J.after(1000,u)
		u();J.mainloop()
	elif R and not P:
		def AJ():
			B=N.reference(f"games/{F}");E=B.get()
			if not E:L.showerror(A4,'Game session data not found.');A2();return
			A=B.child('drawing/nails').get()
			if A:
				C=[]
				for G in AQ(A.keys()):D=A[G];H=D[S];I=D['y'];C.append((H,I))
				BT(C)
			else:L.showerror(A4,'No drawing data found.');A2();return
		AJ()
		def v():
			if not Y[W]:return
			global a
			if a:return
			D=N.reference(f"games/{F}");B=D.get()
			if not B:return
			if B.get(U)==j:Y[W]=h;J.after(0,lambda:t(F,l))
			elif B.get(U)==A5:
				L.showinfo('Drawing Updated','The drawer is updating the drawing.')
				try:A.clear()
				except K.Terminator:A=K.Screen();A.setup(width=G(I[T].split(S)[0]),height=G(I[T].split(S)[1]));A.bgcolor(I[p]);A.title(AF);C=K.Turtle();C.speed(0);C.hideturtle()
				Aj(F);return
			else:J.after(1000,v)
		v();BQ(F,J,f)
	else:
		C.onscreenclick(lambda x,y:BP(x,y))
		if not E or not E.winfo_exists():
			E=B.CTk();E.title(k);Z,n=map(G,I[T].split(S));E.geometry(f"{Z}x150")
			for d in E.winfo_children():d.destroy()
			g=B.CTkFrame(E,corner_radius=10);g.pack(fill=b,padx=20,pady=10);z=B.CTkLabel(g,text='Time: 0',font=(H,16));z.pack(side=V,padx=10);AK=B.CTkButton(g,text=B7,font=(H,16),command=lambda:[A1(),s()]);AK.pack(side='right',padx=10)
			def A0():
				global a
				if a:return
				A=G(e.time()-w)if w else 0;z.configure(text=f"Time: {A} sec");E.after(1000,A0)
			A0();E.mainloop()
def BN(is_multiplayer,is_drawing,game_session_id=F):
	F=is_drawing;E=is_multiplayer;B=game_session_id;global A,D,M,C;A.clear();D=[];M=0
	if E and F:
		H=N.reference(f"games/{B}/drawing");H.delete();J=N.reference(f"games/{B}");J.update({U:A5});L.showinfo('Canvas Reset','Your canvas has been reset.')
		try:C.reset()
		except K.Terminator:C=K.Screen();C.setup(width=G(I[T].split(S)[0]),height=G(I[T].split(S)[1]));C.bgcolor(I[p]);C.title(AF);A=K.Turtle();A.speed(0);A.hideturtle()
		A=K.Turtle();A.speed(0);A.hideturtle();C.onscreenclick(lambda x,y:AM(x,y,E,F,B))
def AL(is_multiplayer,is_drawing,game_session_id=F):
	A=game_session_id;global D,i,C
	if is_multiplayer and is_drawing:
		if m(D)<2:L.showwarning('Not Enough Nails','Please place at least 2 nails before sending the drawing.');return
		B=N.reference(f"games/{A}/drawing/nails");B.delete()
		for E in D:B.push({S:E[0],'y':E[1]})
		F=N.reference(f"games/{A}");F.update({U:AE});L.showinfo('Drawing Sent','Your drawing has been sent to the guesser.');i=h
		if not hasattr(AL,B6):Ak(A);AL.chat_window_opened=Q
def BO(is_multiplayer,is_drawing,game_session_id=F):
	D=game_session_id;B=is_drawing;A=is_multiplayer;global i,C
	if A and B:
		i=Q;L.showinfo('Edit Mode','You can now add more nails to your drawing.');F=N.reference(f"games/{D}");F.update({U:A5})
		try:C.reset()
		except K.Terminator:C=K.Screen();C.setup(width=G(I[T].split(S)[0]),height=G(I[T].split(S)[1]));C.bgcolor(I[p]);C.title(AF);E=K.Turtle();E.speed(0);E.hideturtle()
		Al();C.onscreenclick(lambda x,y:AM(x,y,A,B,D))
def AM(x,y,is_multiplayer,is_drawing,game_session_id=F):
	global D,M,O,i
	if M<O or i:
		B=W[q];A.penup();A.goto(x,y);A.pendown();A.dot(W[g],B);D.append((x,y));M+=1
		if M>=O and not i:Al()
		else:0
	else:L.showinfo(AZ,Aa)
def BP(x,y):
	global D,M,O,A
	if M<O:
		B=W[q];A.penup();A.goto(x,y);A.pendown();A.dot(W[g],B)
		if D:A.color(X[n]);A.pensize(X[k]);A.penup();A.goto(D[-1]);A.pendown();A.goto(x,y);A.penup();A.color(B)
		D.append((x,y));M+=1
		if M==O:A.color(X[n]);A.pensize(X[k]);A.penup();A.goto(D[-1]);A.pendown();A.goto(D[0]);A.penup();A.color(B)
	else:L.showinfo(AZ,Aa)
def BQ(game_session_id,game_root,timer_label):
	C=game_session_id;global P;P=B.CTkToplevel();P.title('Guess the Drawing');P.geometry('400x400');D=B.CTkFrame(P);D.pack(expand=Q,fill=b,padx=10,pady=10);F=B.CTkFrame(D);F.pack(fill=S,padx=5,pady=5);I=B.CTkLabel(F,text='Time left: 120',font=(H,14));I.pack(side=V,padx=5);A=R.Text(D,state=u,wrap=Ab,height=10);A.pack(expand=Q,fill=b);E=B.CTkFrame(P);E.pack(fill=S,padx=10,pady=5);J=R.StringVar();L=B.CTkEntry(E,textvariable=J);L.pack(side=V,fill=S,expand=Q,padx=(0,5));M=B.CTkButton(E,text=B1,command=lambda:Af(A9));M.pack(side=V,padx=10)
	def O(guess):
		B=guess;B=B.strip()
		if B:
			D=N.reference(f"games/{C}");E=D.get();H=E.get(x,o).lower();F=B.lower()==H.lower();G=E.get(A7,0)+1;I=D.child(AV);K={AU:B,B8:F};I.push(K)
			if F:D.update({U:j,AD:'Guesser Won',AY:e.time(),A7:G});A.config(state=AG);A.insert(z,f"You: {B}\n");A.insert(z,"Correct! You've guessed the drawing.\n");A.config(state=u);AP();P.after(0,lambda:t(C,l))
			else:D.update({A7:G});A.config(state=AG);A.insert(z,f"You: {B}\n");A.insert(z,'Incorrect guess. Try again.\n');A.config(state=u);J.set(o)
	def K():
		global Ba;B=N.reference(f"games/{C}");A=B.get()
		if not A:return
		D=G(e.time()-A.get(A6,e.time()));E=max(0,120-D);I.configure(text=f"Time left: {E}s")
		if A.get(U)==j:AP();P.after(0,lambda:t(C,l));return
		else:P.after(1000,K)
	K();BR(C)
def BR(game_session_id):
	global d;d=B.CTkToplevel();d.title('Hints');d.geometry('300x200');D=B.CTkFrame(d);D.pack(expand=Q,fill=b,padx=10,pady=10);A=R.Text(D,state=u,wrap=Ab,height=10);A.pack(expand=Q,fill=b);C=F
	def E():
		nonlocal C;B=N.reference(f"games/{game_session_id}");D=B.child(A8).get()
		if D:
			H=AQ(D.items(),key=lambda x:x[0])
			for(G,I)in enumerate(H):
				if C is F or G>C:J=I[1][AX];A.config(state=AG);A.insert(z,f"{J}\n");A.config(state=u);C=G
		K=B.get()
		if K.get(U)==j:d.destroy()
		else:d.after(1000,E)
	E()
def Ak(game_session_id):
	D=game_session_id;global P;P=B.CTkToplevel();P.title("Guesser's Attempts");P.geometry(AW);E=B.CTkFrame(P);E.pack(expand=Q,fill=b,padx=10,pady=10);A=R.Text(E,state=u,wrap=Ab);A.pack(expand=Q,fill=b);C=F
	def G():
		nonlocal C;I=N.reference(f"games/{D}");B=I.get();J=B.get(AV,{});K=AQ(J.items(),key=lambda item:item[0])
		for(E,H)in K:
			if C is F or E>C:L=H[AU];M=H[B8];A.config(state=AG);A.insert(z,f"Guesser guessed: {L}\n");A.config(state=u);C=E
		if B.get(U)==j:AP();P.after(0,lambda:t(D,r))
		else:P.after(1000,G)
	G()
def BS():
	global O
	while Q:
		try:
			A=B.CTkInputDialog(text=B9,title=BA).get_input();O=G(A)
			if O>0:break
			else:L.showerror(AH,BB)
		except(A3,Ap):L.showerror(AH,BC)
	return O
def Al():
	global A,D;A.color(X[n])
	for(C,E)in D:A.penup();A.goto(C,E);A.pendown();A.dot(W[g],W[q])
	for B in AR(m(D)):F,G=D[B];H,I=D[(B+1)%m(D)];A.penup();A.goto(F,G);A.pendown();A.pensize(X[k]);A.goto(H,I)
	global M;M=0
def BT(nails_list):
	B=nails_list;A.clear();A.color(X[n])
	for(D,E)in B:A.penup();A.goto(D,E);A.pendown();A.dot(W[g],W[q])
	for C in AR(m(B)):F,G=B[C];H,I=B[(C+1)%m(B)];A.penup();A.goto(F,G);A.pendown();A.pensize(X[k]);A.goto(H,I)
def BU():
	V='Digital String Art - Free Draw Mode';global A,C,D,M,O,E;A1()
	if not C or not C._root:C=K.Screen()
	else:
		try:C.reset()
		except K.Terminator:C=K.Screen()
	C.setup(width=G(I[T].split(S)[0]),height=G(I[T].split(S)[1]));C.bgcolor(I[p]);C.title(V);A=K.Turtle();A.speed(0);A.hideturtle();E=B.CTk();E.title(V);Y,l=map(G,I[T].split(S));E.geometry(f"{Y}x200");F=B.CTkFrame(E,corner_radius=10);F.pack(fill=b,padx=20,pady=10);B.CTkLabel(F,text=Aw,font=(H,12)).grid(row=0,column=0,padx=5,pady=5);P=R.IntVar(value=W[g]);Z=B.CTkEntry(F,textvariable=P,width=50);Z.grid(row=0,column=1,padx=5,pady=5)
	def a():
		A=A0.askcolor(title=Ax)
		if A:W[q]=A[1]
	c=B.CTkButton(F,text=Ay,command=a);c.grid(row=0,column=2,padx=5,pady=5);B.CTkLabel(F,text='String Thickness:',font=(H,12)).grid(row=1,column=0,padx=5,pady=5);Q=R.IntVar(value=X[k]);d=B.CTkEntry(F,textvariable=Q,width=50);d.grid(row=1,column=1,padx=5,pady=5)
	def e():
		A=A0.askcolor(title=Az)
		if A:X[n]=A[1]
	f=B.CTkButton(F,text=A_,command=e);f.grid(row=1,column=2,padx=5,pady=5);N=B.CTkButton(F,text=B5,command=lambda:An(J));N.grid(row=0,column=3,padx=5,pady=5)
	def h():A=C.getcanvas();A.postscript(file='string_art.eps');L.showinfo('Export Successful',"Your art has been exported as 'string_art.eps'.")
	i=B.CTkButton(F,text='Export Canvas',command=h);i.grid(row=1,column=3,padx=5,pady=5);J=B.CTkLabel(F,text=AC,font=(H,14));J.grid(row=0,column=4,rowspan=2,padx=10,pady=5);N=B.CTkButton(F,text=B0,command=lambda:An(J));N.grid(row=0,column=3,padx=5,pady=5);j=B.CTkButton(F,text=B7,command=lambda:[A1(),s()]);j.grid(row=0,column=5,rowspan=2,padx=10,pady=5);AN()
	def U():
		try:W[g]=G(P.get())
		except A3:W[g]=10
		try:X[k]=G(Q.get())
		except A3:X[k]=2
		E.after(500,U)
	U();C.onscreenclick(lambda x,y:Am(x,y,J));E.mainloop()
def AN():
	global O
	while Q:
		try:
			A=B.CTkInputDialog(text=B9,title=BA).get_input();O=G(A)
			if O>0:break
			else:L.showerror(AH,BB)
		except(A3,Ap):L.showerror(AH,BC)
	return O
def Am(x,y,cost_label):
	C=cost_label;global D,M,O,A
	if M<O:
		B=W[q];A.penup();A.goto(x,y);A.pendown();A.dot(W[g],B)
		if D:A.color(X[n]);A.pensize(X[k]);A.penup();A.goto(D[-1]);A.pendown();A.goto(x,y);A.penup();A.color(B)
		D.append((x,y));M+=1
		if M==O:
			A.color(X[n]);A.pensize(X[k]);A.penup();A.goto(D[-1]);A.pendown();A.goto(D[0]);A.penup();A.color(B)
			if C:E=BV();C.configure(text=f"Total Cost: ${E:.2f}")
	else:L.showinfo(AZ,Aa)
def BV():
	global D;C=5.;E=m(D)*.12;A=0
	for B in AR(m(D)):F,G=D[B];H,I=D[(B+1)%m(D)];J=((H-F)**2+(I-G)**2)**.5;A+=J
	K=A/32*.07;L=C+E+K;return L
def An(cost_label):
	B=cost_label;global A,D,M,C;A.clear();D=[];M=0
	if B:B.configure(text=AC)
	AN()
def BW():
	A=B.CTkToplevel();A.title(Au);C=R.StringVar(value=I[T]);B.CTkLabel(A,text='Resolution:',font=(H,12)).pack(pady=5);E=['800x600',Aq,'1280x720','1366x768','1600x900','1920x1080'];B.CTkOptionMenu(A,variable=C,values=E).pack(pady=5);B.CTkLabel(A,text='Background Color:',font=(H,12)).pack(pady=5)
	def F():
		A=A0.askcolor(title='Choose Background Color')
		if A:I[p]=A[1]
	G=B.CTkButton(A,text='Choose Color',command=F);G.pack(pady=5);D=R.BooleanVar(value=I[AS]);B.CTkLabel(A,text='Enable Audio',font=(H,12)).pack(pady=5);B.CTkSwitch(A,text='Audio',variable=D).pack(pady=5)
	def J():I[T]=C.get();I[AS]=D.get();A.destroy();L.showinfo('Settings Saved','Your settings have been updated.')
	B.CTkButton(A,text='Save',command=J).pack(pady=10)
def BX():
	m='Close';l='<Button-1>';k='hand2';j='blue';i='https://yair.ca';h='#6C757D';g='History & Development';e='#FFC107';d='Tech Stack';c='- Customizable nail and string settings (color, size, thickness).\n- Export your creations as high-quality images.\n- Real-time multiplayer with chat and synchronization.';a='#28A745';Z='Features';Y='#FF6347';X='Game Modes';W='#007BFF';U='Digital String Art Platform v1.0';T='Digital String Art Platform - Info';S='radiance';B='Helvetica';C=Ad(theme=S);C.title(T);C.geometry('600x725');A=J.Frame(C,padding=10);A.pack(fill=b,expand=Q);E=J.Label(A,text=U,font=(B,22,f),foreground=W);E.pack(pady=10);F=J.Label(A,text='Welcome to Digital String Art Platform v1.0, the place where art meets technology! This app allows you to create interactive string art using customizable tools and play with friends in different game modes. Developed by Yair K., this app is designed to be fun, competitive, and collaborative.',font=(B,12),wraplength=580,justify=V);F.pack(pady=5);G=J.Label(A,text=X,font=(B,16,f),foreground=Y);G.pack(pady=10);H=J.Label(A,text='- Free Draw Mode: Unleash your creativity with a freeform drawing experience.\n- Multiplayer Mode: Compete with friends online in a guessing game.\n- Vs AI Mode: Play against our AI to test your skills.',font=(B,12),wraplength=580,justify=V);H.pack(pady=5);I=J.Label(A,text=Z,font=(B,16,f),foreground=a);I.pack(pady=10);K=J.Label(A,text=c,font=(B,12),wraplength=580,justify=V);K.pack(pady=5);L=J.Label(A,text=d,font=(B,16,f),foreground=e);L.pack(pady=10);M=J.Label(A,text='- Python for core functionality.\n- Turtle Graphics for rendering.\n- CustomTkinter for sleek UI.\n- GPT-4o for clever AI Recognition\n- Google Firebase Database for real-time multiplayer support.',font=(B,12),wraplength=580,justify=V);M.pack(pady=5);N=J.Label(A,text=g,font=(B,16,f),foreground=h);N.pack(pady=10);O=J.Label(A,text='The DSAP was created by Yair as an extention to his 1P13A Project. He got tired from being tired from studying for his midterms so he decided to make studying even harder by taking on this project.',font=(B,12),wraplength=580,justify=V);O.pack(pady=5)
	def P(event):Ae.open_new(i)
	D=J.Label(A,text='Feel free to visit my Portfolio @ https://yair.ca',font=(B,14,f),foreground=j,cursor=k);D.pack(pady=10);D.bind(l,P);R=J.Button(C,text=m,command=C.destroy);R.pack(pady=20);C.mainloop();C=Ad(theme=S);C.title(T);C.geometry('600x700');A=J.Frame(C,padding=10);A.pack(fill=b,expand=Q);E=J.Label(A,text=U,font=(B,22,f),foreground=W);E.pack(pady=10);F=J.Label(A,text='Welcome to Digital String Art v1.0, the platform where art meets technology! This app allows you to create interactive string art using customizable tools and play with friends in different game modes. Developed by Yair K., this app is designed to be fun, competitive, and collaborative.',font=(B,12),wraplength=580,justify=V);F.pack(pady=5);G=J.Label(A,text=X,font=(B,16,f),foreground=Y);G.pack(pady=10);H=J.Label(A,text='- Free Draw Mode: Unleash your creativity with a freeform drawing experience.\n- Multiplayer Mode: Compete with friends in a guessing game.\n- Vs AI Mode (Coming Soon): Play against our AI to test your skills.',font=(B,12),wraplength=580,justify=V);H.pack(pady=5);I=J.Label(A,text=Z,font=(B,16,f),foreground=a);I.pack(pady=10);K=J.Label(A,text=c,font=(B,12),wraplength=580,justify=V);K.pack(pady=5);L=J.Label(A,text=d,font=(B,16,f),foreground=e);L.pack(pady=10);M=J.Label(A,text='- Python for core functionality.\n- Turtle Graphics for rendering.\n- CustomTkinter for sleek UI.\n- Firebase for real-time multiplayer.',font=(B,12),wraplength=580,justify=V);M.pack(pady=5);N=J.Label(A,text=g,font=(B,16,f),foreground=h);N.pack(pady=10);O=J.Label(A,text='The Digital String Art Platform was created by Yair K.. It has since evolved into a more collaborative experience.',font=(B,12),wraplength=580,justify=V);O.pack(pady=5)
	def P(event):Ae.open_new(i)
	D=J.Label(A,text='Visit my website: yair.ca',font=(B,14,f),foreground=j,cursor=k);D.pack(pady=10);D.bind(l,P);R=J.Button(C,text=m,command=C.destroy);R.pack(pady=20);C.mainloop()
def AO():
	global D,M,O,w,i;global A,C,E,c,Z,P,d,a;D=[];M=0;O=0;w=F;i=h;a=h
	if A:
		try:A.clear();A.reset();A.hideturtle()
		except(K.Terminator,R.TclError):pass
		A=F
	if C:
		try:C.clear();C.bye();C=F
		except(K.Terminator,R.TclError):C=F
	if E:
		try:
			if E.winfo_exists():E.destroy()
		except R.TclError:pass
		E=F
	if c:
		try:
			if c.winfo_exists():c.destroy()
		except R.TclError:pass
		c=F
	if Z:
		try:
			if Z.winfo_exists():Z.destroy()
		except R.TclError:pass
		Z=F
	if P:
		try:
			if P.winfo_exists():P.destroy()
		except R.TclError:pass
		P=F
	if d:
		try:
			if d.winfo_exists():d.destroy()
		except R.TclError:pass
		d=F
def A1():AO()
def A2():A=N.reference(AT);A.child(Y).delete();AO();s()
def BY(game_session_id,is_multiplayer):
	if is_multiplayer:A=N.reference(f"games/{game_session_id}");A.update({U:j})
	AO();s()
def t(game_session_id,player_role):
	global a
	if a:return
	a=Q;K=N.reference(f"games/{game_session_id}");A=K.get()
	if not A:A2();return
	E=A.get(AD,'Unknown');F=A.get(A7,0);I=G(A.get(AY,e.time())-A.get(A6,e.time()));C=B.CTkToplevel();C.title('Game Stats');C.geometry(AW);D=B.CTkFrame(C);D.pack(expand=Q,fill=b,padx=20,pady=20)
	if player_role==l:J=f"Game Over!\nResult: {E}\nTotal Time: {I} seconds\nGuess Attempts: {F}"
	else:J=f"Game Over!\nThe guesser has {E.lower()}.\nTotal Time: {I} seconds\nGuess Attempts: {F}"
	B.CTkLabel(D,text=J,font=(H,16),wraplength=360).pack(pady=20);B.CTkButton(D,text='Return to Lobby',command=lambda:[C.destroy(),A2()]).pack(pady=10)
def AP():
	global E,c,P,d;B=[E,c,P,d]
	for A in B:
		try:
			if A and A.winfo_exists():A.destroy()
		except R.TclError:pass
	if C:
		try:C.bye()
		except K.Terminator:pass
s()