#!/usr/bin/python
import sys,time,struct,rle,mtf,bwt,cli,os

def recordTime(f):
	def w(*a):
		start = time.time()
		f(*a)
		stop = time.time()
		print("Completed in %f s" % (stop-start))
	return w

@recordTime
def compressFile(filename):
	pass

@recordTime
def decompress(filename):
	pass

@recordTime
def rlecompress(infile):
	print("Run Length Encoding	 file %s.." % infile)
	outfile = infile + ".rle"
	rle.encodeFile(infile, outfile)
	inisize = os.stat(infile).st_size
	finsize = os.stat(outfile).st_size
	print("Original filesize: %d" % (inisize))
	print("Final filesize: %d" % (finsize))
	print("%f%% Compressed." % ((1-(float(finsize)/inisize))*100))

@recordTime
def rledecompress(filename):
	print("De-Compressing file %s" % filename)
	rle.decodeFile(filename, filename[:-4]+".lulz")

@recordTime
def mtfencode(filename):
	print("Move to front Encoding file %s.." % filename)
	mtf.encodeFile(filename, filename + ".mtf")

@recordTime
def mtfdecode(filename):
	print("Move to front Decoding file %s" % filename)
	mtf.decodeFile(filename, filename[:-4]+".lulz")

@recordTime
def bwtencode(filename):
	print("BWT-ing file %s" % filename)
	fi = open(filename,"rb").read()
	bwttransform = bwt.encode(fi)
	
	fo = open(filename+".bwt","wb")
	fo.write(struct.pack('i',bwttransform[0]))
	fo.write(struct.pack('c'*len(bwttransform[1]),*bwttransform[1]))
	fo.close()

@recordTime
def bwtdecode(filename):
	print("Reverse BWT-ing file %s" % filename)
	fi = open(filename,"rb")
	n = struct.unpack('i',fi.read(4))[0]
	c = fi.read()
	fi.close()
	fo = open(filename[:-4]+".lulz","wb")
	fo.write(bwt.decode((n,c)))
	fo.close()

if __name__ == '__main__':
	if len(sys.argv) == 3:
		action = sys.argv[1]
		filename = sys.argv[2]

		if action == "c":
			compressFile(filename)
		elif action == "d":
			decompress(filename)
		elif action == "rle":
			rlecompress(filename)
		elif action == "unrle":
			rledecompress(filename)
		elif action == "mtf":
			mtfencode(filename)
		elif action == "unmtf":
			mtfdecode(filename)
		elif action == "bwt":
			bwtencode(filename)
		elif action == "unbwt":
			bwtdecode(filename)
		else:
			cli.usage()
	else:
		cli.usage()
