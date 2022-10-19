import hashlib
import random
import copy
from sys import call_tracing
import time
from tkinter import E
from tokenize import Double
from ecdsa import SigningKey

target = "000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
miner_number=0

def hash(strr):
    var= hashlib.sha256()
    var.update(strr.encode())
    return var.hexdigest()


#######################################             MINER CLASS          ##############################################
class miner:
    def __init__(self):
        global miner_number
        self.miner_index=miner_number
        miner_number=miner_number+1
        self.wallet=wallet(self)
        self.conn_miner=[]
        self.conn_user=[]
        self.blocks=[]
        self.mempool=[]
        self.prev_hash="0000000000000000000000000000000000000000000000000000000000000000"
    
    def add_neigh(self,lisst):
        self.conn_miner.extend(lisst)
        self.conn_miner.remove(self)

#-------------------------------------      PUSHING TRANSACTION IN MEMPOOLS      ------------------------------------------#

    
    def take_transaction(self,obj,transact,sign):

        
        ##############     Verifying the Sign     ###############
        verifying_string=str(transact[1])+str(transact[2])+str(transact[0])
        verification_result=False
        try :
            verification_result=obj.public_key.verify(sign,verifying_string.encode())
        except:
            verification_result=False
        if(verification_result==False):
            return 0
        else :
            check_reciver=False
            for a in self.conn_user:
                if(a.wallet.address==transact[2]):
                    check_reciver=True
            for b in self.conn_miner:
                for a in b.conn_user:
                    if(a.wallet.address==transact[2]):
                        check_reciver=True
            if(not check_reciver):
                return 2
        ###############       Send verified transaction to all miners   ############
            self.mempool.append(transact)
            for rest_miners in self.conn_miner:
                rest_miners.mempool.append(transact)
        return 1



#-------------------------------------      CALCULATING MERKLEROOT      ------------------------------------------#    
    def calculate_merkleroot(self,bodyy):
        listt=[]
        b=0
        for a in bodyy:
            listt.append(hash(str(a[1])+str(a[2])+str(a[0])))
        while(len(listt)>1):
            lisst=[]
            st=""
            for a in listt:
                if(st==""):
                    st=a
                else :
                    st+=a
                    lisst.append(hash(st))
                    st=""
            if(st!=""):
                lisst.append(hash(st))
            listt=lisst
        return listt[0]



#-------------------------------------      CREATING BLOCK AND UPDATING BLOCKCHAIN      ------------------------------------------#
    def create_block(self):
        new_block=block()
        new_block.timestamp=time.time()
        new_block.prev_hash=self.prev_hash
        new_block.nounce=0
        new_block.body=copy.deepcopy(self.mempool)
        
        if(len(self.blocks)!=0):
            new_block.block_index=self.blocks[-1].block_index+1
        new_block.merkleroot=self.calculate_merkleroot(new_block.body)
        self.mempool.clear()
        timedeff=time.time()
        current_hash=hash(str(new_block))
        while(current_hash>str(target)):
            new_block.nounce+=1
            current_hash=hash(str(new_block))
        timedeff-=time.time()
        timedeff=abs(timedeff)
        new_block.current_hash=current_hash
        for i in range(len(new_block.body)):
            new_block.body[i].extend(["Miner"+str(self.miner_index)])
            new_block.body[i].extend([hash(str(new_block.body[i][1])+str(new_block.body[i][2])+str(new_block.body[i][0]))])
        self.blocks+=[new_block]
        self.prev_hash=current_hash
        return [timedeff]


#######################################             WALLET CLASS         ##############################################
class wallet:

    def __init__(self,miner1:miner):
        self.private_key=SigningKey.generate()
        self.public_key=self.private_key.verifying_key
        print(self.private_key.to_string().hex())
        print(self.public_key.to_string().hex())
        self.address=hash(self.public_key.to_string().hex())
        self.utxo = [[100,self.address,self.address]]
        self.utxo=sorted(self.utxo,key=lambda x:x[0])
        self.conn_miner=miner1


#-------------------------------------      INITIATING THE TRANSACTION FROM WALLET      ------------------------------------------#
    def transaction(self,s_number,r_number,r_address,amount,t_fee,r_name):
        listt = []
        total_amount = amount
        amount+=t_fee
        for i in range(len(self.utxo)):
            if (amount>=self.utxo[i][0]):
                amount-=self.utxo[i][0]
                listt.append(i)
            elif(amount==0):
                break
            else:
                self.utxo.append([self.utxo[i][0]-amount,self.address,self.address])
                amount=0
                listt.append(i)
                break
        if(amount>0):
            print("User"+str(s_number)+" don't have sufficient UTXOs")
            return False
        else:
            for i in listt:
                self.utxo.pop(0)
            transact=[total_amount,self.address,r_address,s_number,r_number,t_fee,r_name]
            string_transaction=str(transact[1])+str(transact[2])+str(transact[0])
            signn=self.private_key.sign(string_transaction.encode())
            check=self.conn_miner.take_transaction(self,transact,signn)
            if(check==0):
                self.utxo.append([total_amount+t_fee,self.address,self.address])
                print("Transaction cannot be verifiyied")
                return False
            elif (check == 2):
                self.utxo.append([total_amount+t_fee,self.address,self.address])
                print("User"+str(r_number)+"doesn't exist")
                return False
            return True



#######################################             USER CLASS           ##############################################
class user:
    def __init__(self,miner1:miner()):
        self.wallet=wallet(miner1)
        miner1.conn_user.extend([self])


#######################################             BLOCK CLASS          ##############################################
class block:
    def __init__(self):
    #////////////////////////////            Head             //////////////////////////#
        self.timestamp=0.0
        self.prev_hash=target
        self.current_hash="0000000000000000000000000000000000000000000000000000000000000000"
        self.nounce=0
        self.block_index=0
        self.merkleroot=""
    #///////////////////////////             Body              /////////////////////////#
        self.body=[]
    
    def __str__ (self):
        stringg=""
        for aa in self.body:
            stringg=str(aa[1])+str(aa[2])+str(aa[0])
        return str(self.timestamp)+str(self.prev_hash)+str(self.nounce)+str(self.block_index)+str(self.merkleroot)+stringg
    
    def printt(self):
        print("Block Index : ",self.block_index+1)
        print("Timestamp : ",self.timestamp)
        print("Previous Hash : ",self.prev_hash)
        print("Nounce : ",self.nounce)
        print("MerkleRoot : ",self.merkleroot)
        print("Current Hash : ",self.current_hash)
        print("Transactions : ")
        for a in self.body:
            print("Transaction Hash :       "+str(a[-1]))
            print("Transaction :            User"+str(a[3])+"  Paid  "+str(a[0])+" btc  to  User"+str(a[4])+"  and Paid  "+str(a[-4])+" btc  as transaction fee to "+a[-2])
        print()

########################################         CONSENSUS ALGORITHM           #############################
def consensus(miner_list,user_list):
    array=[]
    for a in miner_list:
        timee=a.create_block()
        timee.extend([a])
        array.append(timee)
    array=sorted(array,key=lambda x:x[0])
    for transact in array[0][1].blocks[-1].body:
        user_list[transact[-5]-1].wallet.utxo.append([transact[0],transact[1],transact[2]])
        array[0][1].wallet.utxo.append([transact[-4],transact[1],array[0][1].wallet.address])
    for a in miner_list:
        if(a!=array[0][1]):
            a.blocks=copy.deepcopy(array[0][1].blocks)
            a.prev_hash=array[0][1].prev_hash

def print_block(blockchain):
    for a in blockchain:
        a.printt()

if __name__ == "__main__" :


#````````````````````````````             create 10 miners            ``````````````````````````#
    miner1=miner()
    miner2=miner()
    miner3=miner()
    miner4=miner()
    miner5=miner()
    miner6=miner()
    miner7=miner()
    miner8=miner()
    miner9=miner()
    miner10=miner()

    
#``````````````````````                   connect All miners with each other                 `````````````````````#
    miner_list=[miner1,miner2,miner3,miner4,miner5,miner6,miner7,miner8,miner9,miner10]
    miner2.add_neigh(miner_list)
    miner3.add_neigh(miner_list)
    miner4.add_neigh(miner_list)
    miner5.add_neigh(miner_list)
    miner1.add_neigh(miner_list)
    miner6.add_neigh(miner_list)
    miner7.add_neigh(miner_list)
    miner8.add_neigh(miner_list)
    miner9.add_neigh(miner_list)
    miner10.add_neigh(miner_list)


#``````````````````````              create 20 users and connect them with miners            `````````````````````#
    user1,user2=user(miner1),user(miner1)
    user3,user4=user(miner2),user(miner2)
    user5,user6=user(miner3),user(miner3)
    user7,user8=user(miner4),user(miner4)
    user9,user10=user(miner5),user(miner5)
    user11,user12=user(miner6),user(miner6)
    user13,user14=user(miner7),user(miner7)
    user15,user16=user(miner8),user(miner8)
    user17,user18=user(miner9),user(miner9)
    user19,user20=user(miner10),user(miner10)
    user_list=[user1,user2,user3,user4,user5,user6,user7,user8,user9,user10,user11,user12,user13,user14,user15,user16,user17,user18,user19,user20]
    


#############################            INITIATE THE TRANSACTIONS FROM HERE            #####################################
    while 1 :
        print()
        print("To Send Money press 1 : ")
        print("To See Full Blockchain press 2 : ")
        print("To See Wallet balance press 3 : ")
        print("To exit the code press 0 : ")
        b=int(input())
        if(b==1):
            print("Give the number of transactions you wan't to do : ")
            a = float(input())
            a=int(a)
            check_final=False
            while a>0:
                print("Input transaction in below format :")
                print("For User 1 to User 2 send 3 bitcoin with transaction fee 4 bitcoin write")
                print("1 2 3 4")
                print()
                lst = list(map(float, input().split()))
                if(lst[0]<21 and lst[1]<21):
                    lst[0]=int(lst[0])
                    lst[1]=int(lst[1])
                    check=user_list[lst[0]-1].wallet.transaction(lst[0],lst[1],user_list[lst[1]-1].wallet.address,lst[2],lst[3],user_list[lst[1]-1])
                    check_final=check_final or check
                else:
                    print("Users not valid")
                a-=1
            if(check_final):
                consensus(miner_list,user_list)
        elif b==2:
            print("The blockchain so for looks like below")
            print_block(miner1.blocks)
        elif b==3:
            print("To see Wallet balance of User x press ")
            print("0 x")
            print("And to see Wallet balance of Miner y press ")
            print("1 y")
            lst = list(map(int, input().split()))
            if lst[0]==0:
                print(user_list[lst[1]-1].wallet.utxo)
            else:
                print(miner_list[lst[1]-1].wallet.utxo)
        else:
            break