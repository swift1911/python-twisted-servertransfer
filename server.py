from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

list=[]
fdict=dict()
tdict=dict()
listzhuzhan=[]
rdict={}

class SimpleLogger(LineReceiver):

    def connectionMade(self):
        print 'Got connection from', self.transport.client
    def connectionLost(self, reason):
	print self.transport.client, 'disconnected'
	if self.transport in list:
            list.pop(list.index(self.transport))
            print 'remove from list'
        if self.transport in fdict.values():
	    fdict.pop(tdict.get(self.transport))
            print 'remove from fdict'
	if self.transport in listzhuzhan:
            listzhuzhan.pop(listzhuzhan.index(self.transport))
            print 'remove from listzhuzhan'
    def lineReceived(self, line):
        print line
    def dataReceived(self,data):		
	if data=='login':
		listzhuzhan.append(self.transport)
		self.transport.write('login correct')
		print self.transport.client,'login'
	elif data[0:4]=='send':
		addr=str(data[5].encode('hex'))+str(data[4].encode('hex'))+str(int(data[6].encode('hex'),16)+int(data[7].encode('hex'),16)*256)
		print addr
		if len(fdict)==0:
			print 'no client'
		for item in fdict.iterkeys():
			if addr==item:
				self.printout(data,0)
				print 'write to',addr
				fdict.get(addr).write(data[8:len(data)])
				#rdict[addr]=self.transport
				rdict.setdefault(addr,[]).append(self.transport)
				self.printout(data[8:len(data)],1)
				break
			else:
				print 'addr is not online'
	elif data[0:4]=='list':
                print data
		if len(fdict)==0:
                        self.transport.write('no client')
			print 'list is empty'
			print >>f,'list is empty'
		else:
			liststring=''
			for item in fdict.iterkeys():
				liststring+=str(item)
				liststring+=','
			self.transport.write(liststring)
			print 'get list'
			print >>f,'get list'
	elif (int(data[6].encode('hex'),16)&0xf0)>>7==1:
		if data[12]=='\x02':
                        self.printout(data,0)
			data=data[:6]+'\x0b'+data[7:]
			data=data[:12]+'\x00'+data[13:]
			date=data[:13]+'\x60'+data[14:]
			t=0
			for i in range (6,17):
                           t+=int(data[i].encode('hex'),16)
                        data=data[:18]+chr(t&0xff)+data[19:]
                        self.transport.write(data)
			list.append(self.transport)
                        addressadd=str(data[8].encode('hex'))+str(data[7].encode('hex'))+str(int(data[9].encode('hex'),16)+int(data[10].encode('hex'),16)*256)
                        if fdict.has_key(addressadd)==False:   
			    fdict[addressadd]=self.transport
			    tdict[self.transport]=addressadd
                        if fdict.get(addressadd) !=self.transport:
                            fdict[addressadd]=self.transport
			    tdict[self.transport]=addressadd
                            print 'connection has changed'
			self.printout(data,1)
		else:
			if self.transport not in list:
				self.printout(data,0)
                                addressadd=str(data[8].encode('hex'))+str(data[7].encode('hex'))+str(int(data[9].encode('hex'),16)+int(data[10].encode('hex'),16)*256)
                                if fdict.has_key(addressadd)==False:
                                    fdict[addressadd]=self.transport
				    tdict[self.transport]=addressadd
                                    print 'address added:',addressadd
                                    #print fdict
            			if fdict.get(addressadd) !=self.transport:
                                    fdict[addressadd]=self.transport
				    tdict[self.transport]=addressadd
				self.transport.write(data)
				self.printout(data,1)
				list.append(self.transport)
				print 'list added'
				'''sendstr="68 32 00 32 00 68 4B 01 32 B4 37 02 0A 65 00 00 10 0A F4 16"	
				a=self.bytestring(sendstr)
				for item in a:
					self.transport.write(item)
				self.printout(a,1)'''
			else :
				if int(data[6].encode('hex'),16)&0x0f==0x09:
                                	self.printout(data,0)
					self.transport.write(data)
					self.printout(data,1)
				else:
					self.printout(data,0)
					address=str(data[8].encode('hex'))+str(data[7].encode('hex'))+str(int(data[9].encode('hex'),16)+int(data[10].encode('hex'),16)*256)
					#print rdict.get(self.tranport.client)
					temp=rdict.get(address)
					if len(rdict)!=0:
						for i in range(0,len(temp)):
							temp[i].write(data)
						rdict.pop(address)
						print 'remove from rdict'
						self.printout(data,1)
					else:
						print 'package has been dropped'

	else:
		#self.transport.write(data)
                bt=bytearray(data)
                for b in bt:
                    print hex(b),
		print ''
		print (int(data[6].encode('hex'),16)&0xf0)>>7
		print 'error input!'
		#self.transport.write(data)
		
        print 'dict:',fdict
	print >>f,fdict
    def bytestring(self,strdata):
	sarray=strdata.split(' ')
	b=[]
	for s in sarray:
		b.append(chr(int(s,16)))
	return b
    def printout(self,strlist,updown):
	bt=bytearray(strlist)
	for l in bt:
		print hex(l),
	if updown==1:
		print 'down',
	else :
		print 'up',
	print ''	
factory = Factory()
f=open('log.txt','w')
factory.protocol = SimpleLogger
reactor.listenTCP(10004, factory)
reactor.run()
