def program():
    print("""
    1. matrix
    2. singly
    3. doubly
    4. circular
    5. stack
    6. conversion
    7. queue
    8. cirque
    9. sequential
    10. merge
    11. traversal
    12. spanning
""")

def matrix():
    print("""
#include<iostream>
using namespace std;
class matrix
{
	public: int m1[10][10],m2[20][20];
	int r,c,i,j,t;
	void read()
	{
		t=0;
		cout<<"enter the no of rows:"<<endl;
		cin>>r;
		cout<<"enter the no of columns:"<<endl;
		cin>>c;
		cout<<"enter elements of matrix:"<<endl;
		for(i=0;i<r;i++)
		{
			for(j=0;j<c;j++)
			{
				cin>>m1[i][j];
				if(m1[i][j])
				{
					t++;
					m2[t][0]=i+1;
					m2[t][1]=j+1;
					m2[t][2]=m1[i][j];
				}
			}
		}
		m2[0][0]=r;
		m2[0][1]=c;
		m2[0][2]=t;	
	}
	void display()
	{
        cout<<"matrix is:"<<endl;
        for( int i=0;i<r;i++)
        {
            for(j=0;j<c;j++)
            {
                cout<<m1[i][j];
            }
            cout<<"\n";
        }
	}
	void triplet()
	{
		cout<<"sparse matrix triplet is:\n";
		for(i=0;i<=t;i++)
		{
			for(j=0;j<3;j++)
			{
				cout<<m2[i][j]<<" ";
			}
			cout<<"\n";
		
		}
	}
	void transpose()
	{
		int trans[10][5];
		trans[0][0]=m2[0][1];
		trans[0][1]=m2[0][0];
		trans[0][2]=m2[0][2];
		
		int q=1;
		for(i=0;i<=c;i++)
		{
			for(int p=1;p<=t;p++)
			{
				if(m2[p][1]==i)
				{
					trans[q][0]=m2[p][1];
					trans[q][1]=m2[p][0];
					trans[q][2]=m2[p][2];
					q++;
				}
			}
		}
		cout<<"transpose"<<endl;
		for(i=0;i<=t;i++)
		{
			for(j=0;j<3;j++)
			{
				cout<<trans[i][j]<<" ";
			}
			cout<<endl;
		}
	}	
};
int main()
{
	matrix m;
	m.read();
	m.display();
	m.triplet();
	m.transpose();
	return 0;
}
    """)

def singly():
    print("""
#include<iostream> 
using namespace std; 
struct node 
{ 
    int data; 
    struct node*next; 
}; 
node*head=NULL; 
class singly 
{ 
    public: 
    void insertbeg() 
    { 
        cout<<"Enter the Data:"<<"\n"; 
        node*nn=new node; 
        if(head==NULL) 
        { 
            cin>>nn->data; 
            nn->next=NULL; 
            head=nn; 
        } 
        else 
        { 
            cin>>nn->data; 
            nn->next=head; 
            head=nn; 
        } 
    } 
    void display() 
    { 
        node*temp=head; 
        while(temp!=NULL) 
        { 
            cout<<temp->data<<"->"; 
            temp=temp->next; 
        } 
        cout<<"NULL"<<endl; 
    } 
    void insertend() 
    { 
        node*temp=head; 
        cout<<"Enter the Data:"<<"\n"; 
        node*nn=new node; 
        nn->next=NULL; 
        if(head==NULL) 
        { 
            cin>>nn->data; 
            nn->next=NULL; 
            head=nn; 
        } 
        else 
        { 
            while(temp->next!=NULL) 
            { 
                temp=temp->next; 
            } 
            cin>>nn->data; 
            temp->next=nn; 
        } 
    } 

    void insertran() 
    { 
        int loc; 
        node*nn=new node; 
        nn->next=NULL; 
        cout<<"Enter the Location :"<<endl; 
        cin>>loc; 
        cout<<"Enter the data:"<<endl; 
        if(loc<1) 
        { 
            cout<<"Location should be greater than 1:"<<"\n"; 
        } 
        else if(loc==1) 
        { 
            cin>>nn->data; 
            nn->next=head; 
            head=nn; 
        } 
        else 
        { 
            node *temp=head; 
            for(int i=1;i<loc-1;i++) 
            { 
                if(temp!=NULL) 
                { 
                    temp=temp->next; 
                } 
            } 
            if(temp!=NULL) 
            { 
                cin>>nn->data; 
                nn->next=temp->next; 
                temp->next=nn; 
            } 
            else 
            { 
                cout<<"the previous node is null"<<"\n"; 
            } 
        } 
    } 
    void deletebin() 
    { 
        node *temp; 
        if(head==NULL) 
        { 
            cout<<"Underflow Plz First insert a node first\n"<<endl; 
        } 
        else 
        { 
            temp=head; 
            head=head->next; 
            delete temp; 
        } 
    } 
    void deleteend() 
    { 
        node *temp; 
        node *current; 
        if(head==NULL) 
        { 
            cout<<"Underflow Plz First insert a node first\n"<<endl; 
        } 
        else 
        { 
            temp=head; 
            while(temp->next!=NULL) 
            { 
                current=temp; 
                temp=temp->next; 
            } 
            current->next=NULL; 
            delete temp; 
        } 
    } 
    void deleteran() 
    { 
        if(head==NULL) 
        { 
            cout<<"List is Empty please Insert a Node First\n"<<endl; 
        } 
        else 
        { 
            int pos,i=1; 
            node *temp,*nextnode; 
            cout<<"Plz enter Position : "; 
            cin>>pos; 
            temp=head; 
            while(i<pos-1) 
            { 
                temp=temp->next; 
                i++; 
            } 
            nextnode=temp->next; 
            temp->next=nextnode->next; 
            delete nextnode; 
        } 
    } 
}; 
int main() 
{ 
    Linked L1; 
    int ch; 
    while(1) 
    { 
        cout<<"---menu---"<<"\n"; 
        cout<<"1.Insert at Begin"<<"\n"; 
        cout<<"2.Insert at End"<<"\n"; 
        cout<<"3.Insert at random "<<"\n"; 
        cout<<"4.Delete at Begin"<<"\n"; 
        cout<<"5.Delete at End"<<"\n"; 
        cout<<"6.Delete at Random Position\n"; 
        cout<<"7.Exit"<<"\n"; 
        cout<<"Enter choice :";
        cin>>ch; 
        switch(ch) 
        { 
            case 1: 
                L1.insertbeg(); 
                L1.display(); 
                break; 
            case 2: 
                L1.insertend(); 
                L1.display(); 
                break; 
            case 3: 
                L1.insertran(); 
                L1.display(); 
                break; 
            case 4: 
                L1.deletebin(); 
                L1.display(); 
                break; 
            case 5: 
                L1.deleteend(); 
                L1.display(); 
                break; 
            case 6: 
                L1.deleteran(); 
                L1.display(); 
                break; 
            case 7: 
                exit(0); 
                cout<<"Thank You!"; 
        } 
    } 
} 
    """)
def doubly():
    print("""
#include <iostream>
using namespace std;
struct node
{
    int data;
    node* next;
    node* prev;
};
node *head=NULL;
class doubly
{
    public:
    void insertbeg()
    {
        cout<<"Enter the data :"<<endl;
        node *nn=new node;
        nn->next=head;
        nn->prev=NULL;
        if(head==NULL)
        {
            cin>>nn->data;
            head=nn;
        }
        else
        {
            cin>>nn->data;
            head->prev=nn;
            head=nn;
        }
    }
    void displaybeg()
    {
        node *temp=head;
        while (temp!=NULL)
        {
            cout<<temp->data<<"<=>";
            temp=temp->next;
        }
        cout<<"NULL"<<endl;
    }
    void insertend()
    {
        cout<<"Enter the data :"<<endl;
        node *nn=new node;
        nn->next=NULL;
        nn->prev=NULL;
        if(head==NULL)
        {
            cin>>nn->data;
            head=nn;
        }
        else
        {
            cin>>nn->data;
            node *temp=head;
            while(temp->next!=NULL)
            {
                temp=temp->next;
            }
            temp->next=nn;
            nn->prev=temp;
        }
    }

    void displayend()
    {
        node *temp=head;
        while (temp!=NULL)
        {
            cout<<temp->data<<"<=>";
            temp=temp->next;
        }
        cout<<"NULL"<<endl;
    }
    void insertloc()
    {
        int loc;
        node *nn=new node;
        nn->next=NULL;
        nn->prev=NULL;
        cout<<"Enter the Location :"<<endl;
        cin>>loc;
        cout<<"Enter the data :"<<endl;
        if(loc<1)
        {
            cout<<"Location should be greater than 1.\n";
        }
        else if(loc==1)
        {
            cin>>nn->data;
            nn->next=head;
            head->prev=nn;
            head=nn;
        }
        else
        {
            node *temp=head;
            for(int i=1; i<loc-1; i++)
            {
                if(temp!=NULL)
                {
                    temp=temp->next;
                }
            }
            if(temp!=NULL)
            {
                cin>>nn->data;
                nn->next=temp->next;
                nn->prev=temp;
                temp->next=nn;
            }
            if(nn->next!=NULL)
            {
                nn->next->prev=nn;
            }
            else
            {
                cout<<"The previous node is null.\n";
            }
        }
    }
    void displayloc()
    {
        node *temp=head;
        while (temp!=NULL)
        {
            cout<<temp->data<<"<=>";
            temp=temp->next;
        }
        cout<<"NULL"<<endl;
    }
    void deletebeg()
    {
        node *temp;
        if(head==NULL)
        {
            cout<<"Please insert a node first..!";
        }
        else
        {
            temp=head;
            head=head->next;
            delete temp;
        }
        if(head!=NULL)
        {
            head->prev=NULL;
        }
    }
    void deleteend()
    {
        node *temp;
        node *curr;
        if(head!=NULL)
        {
            if(head->next==NULL)
            {
                head=NULL;
            }
            else
            {
                temp=head;
                while(temp->next->next!=NULL)
                {
                    temp=temp->next;
                }
                curr=temp->next;
                temp->next=NULL;
                delete curr;
            }
        }
    }
    void deleteloc()
    {
        int pos;
        cout<<"Enter the Position :"<<endl;
        cin>>pos;
        if(pos < 1)
        {
            cout<<"\nPosition should be >= 1."<<endl;
        }
        else if (pos == 1 && head != NULL)
        {
            node *del_node = head;
            head = head->next;
            delete del_node;
            if(head != NULL)
            {
                head->prev = NULL;
            }
        }
        else
        {
            node *temp = head;
            for(int i = 1; i < pos-1; i++)
            {
                if(temp != NULL)
                {
                    temp = temp->next;
                }
            }
            if(temp != NULL && temp->next != NULL)
            {
                node *del_node = temp->next;
                temp->next = temp->next->next;
                if(temp->next->next != NULL)
                {
                    temp->next->next->prev = temp->next;
                }
                delete del_node;
            }
            else
            {
                cout<<"\nThe node is already null."<<endl;
            }
        }
    }
};


int main()
{
    doubly obj;
    int ch;
    while(1)
    {
        cout<<"1.Insert | 2.Delete | 3.Exit"<<endl;
        cout<<"Enter the choice : ";
        cin>>ch;
        switch (ch)
        {
            case 1: int b;
                cout<<"1.Insert at Beginning|2.Insert at Specific Location|3.Insert at End "<<endl;
                cout<<"Enter the choice : ";
                cin>>b;
                switch(b)
                {
                    case 1: 
                        obj.insertbeg();
                        obj.displaybeg();
                        break;
                    case 2: 
                        obj.insertloc();
                        obj.displayloc();
                        break;
                    case 3: 
                        obj.insertend();
                        obj.displayend();
                        break;
                }
                break;
            case 2: 
                int d;
                cout<<"1.Delete at Beginning|2.Delete at Specific Location|3.Delete at End "<<endl;
                cout<<"Enter the choice : ";
                cin>>d;
                switch(d)
                {
                    case 1: 
                        obj.deletebeg();
                        obj.displaybeg();
                        break;
                    case 2: 
                        obj.deleteloc();
                        obj.displayloc();
                        break;
                    case 3: 
                        obj.deleteend();
                        obj.displayend();
                        break;
                }
                break;
            case 3:
                cout<<"THANK YOU!"<<endl;
                exit(0);
        }
    }
    return 0;
}
	""")

def circular():
    print("""
#include<iostream> 
using namespace std; 

struct node 
{ 
int data; 
node *next; 
}; 
node *head=NULL; 

class circular 
{ 
public: 
//Insert at the END 
void insertend() 
{ 
cout<<"Enter the data :"<<endl; 
node *nn=new node; 
nn->next=NULL; 
if(head==NULL) 
{ 
cin>>nn->data; 
head=nn; 
nn->next=head; 
} 
else 
{ 
cin>>nn->data; 
node *temp=head; 
while (temp->next!=head) 
{ 
temp=temp->next; 
} 
temp->next=nn; 
nn->next=head; 
} 
} 
//Insert at the Specific Location 
void insertloc() 
{ 
int loc; 
node *nn=new node; 
nn->next=NULL; 
node *temp=head; 
cout<<"Enter the Location :"<<endl; 
cin>>loc; 
cout<<"Enter the data :"<<endl; 
if(loc<1) 
{ 
cout<<"Location should be greater than 1.\n"; 
} 
else if(loc==1) 
{ 
if(head==NULL) 
{ 
cin>>nn->data; 
nn->next=head; 
head=nn; 
} 
else 
{ 
while (temp->next!=head) 
{ 
temp=temp->next; 
} 
nn->next=head; 
head=nn; 
temp->next=nn; 
} 
} 
else 
{ 
temp=head; 
for(int i=1; i<loc-1; i++) 
{ 
if(temp!=NULL) 
{ 
temp=temp->next; 
} 
} 
cin>>nn->data; 
nn->next=temp->next; 
temp->next=nn; 
} 
} 
//Insert at the Beginning 
void insertbeg() 
{ 
cout<<"Enter the data :"<<endl; 
node *nn=new node; 
nn->next=NULL; 
if(head==NULL) 

{ 
cin>>nn->data; 
head=nn; 
nn->next=head; 
} 
else 
{ 
cin>>nn->data; 
node *temp=head; 
while (temp->next!=head) 
{ 
temp=temp->next; 
} 
temp->next=nn; 
nn->next=head; 
head=nn; 
} 
} 

void deletebin() 
{ 
if(head==NULL) 
{ 
cout<<"List is Empty please Insert a Node First\n"<<endl; 
} 
if(head!=NULL) 
{ 
if(head->next==head) 
{ 
head=NULL; 
} 
else 
{ 
node *temp=head; 
node *fn=head; 
while(temp->next!=head) 
{ 
temp=temp->next; 
} 
head=head->next; 
temp->next=head; 
delete fn; 
} 
} 
} 
void deleteend() 
{ 
if(head==NULL) 
{ 
cout<<"List is Empty please Insert a Node First\n"<<endl; 
} 
if(head!=NULL) 
{ 
if(head->next==head) 
{ 
head=NULL; 
} 
else 
{ 
node *temp=head; 
while(temp->next->next!=head) 
{ 
temp=temp->next; 
} 
node *ln=temp->next; 
temp->next=head; 
delete ln; 
} 
} 
} 
void deleteran() 
{ 
node *temp=head; 
node *del_node=head; 
int pos; 
cout<<"Enter the Position :"<<endl; 
cin>>pos; 
if(pos < 1) 
{ 
cout<<"\nPosition should be >= 1."<<endl; 
} 
else if (pos == 1) 
{ 
if(head->next==head) 
{ 
head=NULL; 
} 
else 
{ 
while(temp->next->next!=head) 
{ 
temp=temp->next; 
} 
head=head->next; 
temp->next=head; 
delete del_node; 
} 
} 
else 
{ 
temp=head; 
for(int i=1; i<pos-1; i++) 
{ 
temp=temp->next; 
} 
del_node=temp->next; 
temp->next=temp->next->next; 
delete del_node; 
} 
} 
void display() 
{ 
node *temp=head; 
if(temp!=NULL) 
{ 
cout<<"Start"; 
while (1) 
{ 
cout<<"->"<<temp->data; 
temp=temp->next; 
if(temp==head) 
break; 
} 
cout<<"->"<<endl; 
} 
} 
}; 
int main() 
{ 
circular cir; 
int ch; 
while(1) 
{ 
cout<<"1.Insert | 2. Delete | 3.Exit"<<endl; 
cout<<"Enter the choice : "; 
cin>>ch; 
switch (ch) 
{ 
case 1: int b; 
cout<<"1.Insert at Beginning|2.Insert at Specific Location|3.Insert at End "<<endl; 
cout<<"Enter the choice : "; 
cin>>b; 
switch(b) 
{ 
case 1: cir.insertbeg(); 
cir.display(); 
break; 
case 2: cir.insertloc(); 
cir.display(); 
break; 
case 3: cir.insertend(); 
cir.display(); 
break; 
} 
break; 
case 2: int d; 
cout<<"1.Delete at Beginning|2.Delete at Specific Location|3.Delete at End "<<endl; 
cout<<"Enter the choice : "; 
cin>>d; 
switch(d) 
{ 
case 1: cir.deletebin(); 
cir.display(); 
break; 
case 2: cir.deleteran(); 
cir.display(); 
break; 
case 3: cir.deleteend(); 
cir.display(); 
break;  
} 
break; 
case 3: exit(0); 
} 
} 
return 0; 
} 
    """)

def stack():
    print("""
#include<iostream>
using namespace std;
class STACK{
	public:
	int top=-1;
	int max[4];
	int size=4;
    void push()
	{	
	    int no;
		if(top==size-1)
		{
		cout<<"stack is overflow"<<endl;
		}
	    else
		{
	    top++;
		cout<<"enter the elements:"<<endl;
		cin>>no;
		max[top]=no;
		cout<<"inserted:"<<no<<endl;
		}
	}			
			void pop()
			{
				if((max[top])==-1)
				{
					cout<<"stack is underflow"<<endl;
				}
				else
				{	
					cout<<"pop element"<<max[top]<<endl;
					top--;
				}
			}			
			void display()
			{
				if(max[top]==-1)
				{
					cout<<"stack is empty\n";
				}
				else
				{				
					for(int i=top;i>=0;i--)
					{
						cout<<max[i]<<endl;
					}
				}
			}				
};
int main()
{	
 	STACK s1;
 	int ch,no;	
 	do{
 	cout<<"*****DISPLAY MENU****"<<endl;
 	cout<<"1.push"<<endl;
 	cout<<"2.pop"<<endl;
 	cout<<"3.display"<<endl;
 	cout<<"4.Exit"<<endl;	
 		cout<<"enter your choices:"<<endl;
 		cin>>ch;
 		switch(ch)
 		{
 			case 1:				
				s1.push();
				s1.display();
				break;
			case 2: 
				s1.pop();				
				break;							
			case 3:
				s1.display();
				break;							
			case 4:
				cout<<"Exit"<<endl;
				break;																
 		}
 	}while(ch!=4);
 	return 0;
}
    """)

def queue():
    print("""
#include<iostream>
using namespace std;
#define size 3
class Queue
{
	public:int Q[size],no,rear=-1, front=-1;		
	 void Enqueue()
	{			
		cout<<"enter value to insert"<<endl;
		cin>>no;		
		if(rear==size-1)
		{
			cout<<"queue is full"<<endl;
		}
		else if(rear==-1 && front==-1)
			{
			rear++;
			front++;
			Q[rear]=no;
			}
			else
			{
				rear++;
				Q[rear]=no;
			}
	}		
	void Dequeue()
	{	
		if(rear==-1 && front==-1)
		{
			cout<<"queue is empty"<<endl;
		}
		else if(front==rear)
		{	
			cout<<"delete element is:"<<Q[front]<<endl;
			front=-1;
			rear=-1;
		}
		else
		{	
			cout<<"---delete ele is:"<<Q[front]<<endl;
			front++;			
		}
	}
	void Display()
	{		
		if(rear==-1 && front==-1)
		{
			cout<<"queue is empty"<<endl;
		}
		else
		{	
			cout<<"element in queue is:"<<endl;
			for(int i=front;i<=rear;i++)
			{
				cout<<Q[i]<<endl;
			}
		}
	}
};
int main()
{	
 	Queue q1;
 	int ch,no; 	
 	do{
 	cout<<"*****DISPLAY MENU****"<<endl;
 	cout<<"1.Enqueue"<<endl;
 	cout<<"2.Dequeue"<<endl;
 	cout<<"3.Display"<<endl;
 	cout<<"4.Exit"<<endl; 	
 		cout<<"enter your choices:"<<endl;
 		cin>>ch;
 		switch(ch)
 		{
 			case 1:				
				q1.Enqueue();
				break;			
			case 2: 
				q1.Dequeue();				
				break;							
			case 3:
				q1.Display();
				break;							
			case 4:
				cout<<"Exit"<<endl;
				break;									
 		}
 	}while(ch!=4);
 	return 0;
}   
""")
    
def conversion():
    print("""
#include<bits/stdc++.h>
using namespace std;
int prec(char ch)
{
	if(ch=='^')
		return 3;
	else if(ch=='/'||ch=='*')
		return 2;
	else if(ch=='+'||ch=='-')
		return 1;
	else 
		return -1;
}
string infixTopostfix(string s)
{
	stack<char> st;
	string ans = "";
	for(int i=0;i<s.length();i++)
	{
		char ch = s[i];
		if((ch>='a' && ch<='z')||(ch>='A' && ch<='Z')||(ch>='0' && ch<='9'))
			ans+=ch;
		else if(ch=='(')
			st.push('(');
		else if(ch==')')
		{
			while(st.top()!='(')
			{
				ans+=st.top();
				st.pop();
			}
			st.pop();
		}
		else
		{
			while(!st.empty() && prec(s[i])<=prec(st.top()))
			{
				ans+=st.top();
				st.pop();
			}
			st.push(ch);
		}
	}
	while(!st.empty())
	{
		ans+=st.top();
		st.pop();
	}
	return ans;
}
int main()
{
	string s;
	cin>>s;
	cout<<infixTopostfix(s);
	return 0;
}
""")

def cirque():
    print("""
#include<iostream>
using namespace std;

#define size 4
class cirque
{
	public:int Q[size],no,rear=-1, front=-1;				
	 void Enqueue()
	{		
		cout<<"enter value to insert"<<endl;
		cin>>no;		
		if((rear==size-1 && front==0))
		{
			cout<<"queue is full"<<endl;
		}
		else if(rear==-1 && front==-1)		
			{			
			rear++;
			front++;
			Q[rear]=no;
			}
			else //if(rear==size-1 && front!=0)
			{
				rear++;
				Q[rear]=no;
			}
	}	
	void Dequeue()
	{		
		if(rear==-1 && front==-1)
		{
			cout<<"queue is empty"<<endl;
		}
		else if(front==rear)
		{	
			cout<<"delete element is:"<<Q[front]<<endl;
			front=-1;
			rear=-1;
		}
		else
		{	
			cout<<"---delete ele is:"<<Q[front]<<endl;
			front++;			
		}
	}		
	void Display()
	{
		
		if(rear==-1 && front==-1)
		{
			cout<<"queue is empty"<<endl;
		}
		else
		{	
			cout<<"element in queue is:"<<endl;
			for(int i=front;i<=rear;i++)
			{
				cout<<Q[i]<<endl;
			}
		}
	}
};
int main()
 {	
 	cirque q1;
 	int ch,no;	
 	do{
 	cout<<"*****DISPLAY MENU****"<<endl;
 	cout<<"1.Enqueue"<<endl;
 	cout<<"2.Dequeue"<<endl;
 	cout<<"3.Display"<<endl;
 	cout<<"4.Exit"<<endl;
 	
 		cout<<"enter your choices:"<<endl;
 		cin>>ch;
 		switch(ch)
 		{
 			case 1: 				
				q1.Enqueue();
				break;							
			case 2: 
				q1.Dequeue();				
				break;							
			case 3:
				q1.Display();
				break;							
			case 4:
				cout<<"Exit"<<endl;
				break;		
 		}
 	}while(ch!=4);
 	return 0;
 }
""")
    
def sequential():
    print("""
#include <iostream>
using namespace std;
int main() {
    int arr[10],n,key;
    cout<<"Enter array size :";
    cin>>n;
    cout<<"Enter elements :";
    for (int i = 0; i < n; i++) 
    {
        cin>>arr[i];
    }
    cout<<"Enter key to search :";
    cin>>key;
    for (int i = 0; i < n; i++) 
    {
        if (arr[i] == key) 
        {
            cout << "Element is present at index " << i << endl;
            return 0;
        }
    }
    cout << "Element is not present in array" << endl;      
    return 0;
}
""")
    
def merge():
    print("""
#include <iostream>
using namespace std;
void merge(int arr[], int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;
    int L[n1], R[n2];
    for (int i = 0; i < n1; i++)
        L[i] = arr[left + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[mid + 1 + j];
    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}
void mergeSort(int arr[], int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}
void printArray(int A[], int size) {
    for (int i = 0; i < size; i++)
        cout << A[i] << " ";
}
int main() {
    int arr[] = {12, 11, 13, 5, 6, 7};
    int arr_size = sizeof(arr) / sizeof(arr[0]);
    cout << "Given array is \n";
    printArray(arr, arr_size);
    mergeSort(arr, 0, arr_size - 1);
    cout << "\nSorted array is \n";
    printArray(arr, arr_size);
    return 0;
}
""")
    
def traversal():
    print("""
#include <iostream>
using namespace std;
struct Node {
    int data;
    Node *left, *right;
};
Node* newNode(int data) {
    Node* node = new Node;
    node->data = data;
    node->left = node->right = NULL;
    return node;
}
void inorderTraversal(Node* root) {
    if (root == NULL)
        return;
    inorderTraversal(root->left);
    cout << root->data << " ";
    inorderTraversal(root->right);
}
void preorderTraversal(Node* root) {
    if (root == NULL)
        return;
    cout << root->data << " ";
    preorderTraversal(root->left);
    preorderTraversal(root->right);
}
void postorderTraversal(Node* root) {
    if (root == NULL)
        return;
    postorderTraversal(root->left);
    postorderTraversal(root->right);
    cout << root->data << " ";
}
int main() {
    Node* root = newNode(1);
    root->left = newNode(2);
    root->right = newNode(3);
    root->left->left = newNode(4);
    root->left->right = newNode(5);
    cout << "Inorder Traversal: ";
    inorderTraversal(root);
    cout << endl;
    cout << "Preorder Traversal: ";
    preorderTraversal(root);
    cout << endl;
    cout << "Postorder Traversal: ";
    postorderTraversal(root);
    cout << endl;
    return 0;
}
""")
    
def spanning():
    print("""
#include <cstring>
#include <iostream>
using namespace std;
#define INF 9999999
#define V 5
int G[V][V] = {
  {0, 9, 75, 0, 0},
  {9, 0, 95, 19, 42},
  {75, 95, 0, 51, 66},
  {0, 19, 51, 0, 31},
  {0, 42, 66, 31, 0}};
int main() {
  int no_edge;
  int selected[V];
  memset(selected, false, sizeof(selected));
  no_edge = 0;
  selected[0] = true;
  int x;
  int y; 
  cout << "Edge"
     << " : "
     << "Weight";
  cout << endl;
  while (no_edge < V - 1) {
    int min = INF;
    x = 0;
    y = 0;
    for (int i = 0; i < V; i++) {
      if (selected[i]) {
        for (int j = 0; j < V; j++) {
          if (!selected[j] && G[i][j]) {  // not in selected and there is an edge
            if (min > G[i][j]) {
              min = G[i][j];
              x = i;
              y = j;
            }
          }
        }
      }
    }
    cout << x << " - " << y << " :  " << G[x][y];
    cout << endl;
    selected[y] = true;
    no_edge++;
  }
  return 0;
}
""")