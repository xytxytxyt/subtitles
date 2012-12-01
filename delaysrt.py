import datetime
import StringIO

class Subtitle(object):
	count = None
	fromt = None
	tot = None
	subs = None

	def __init__(self, count, fromt, tot, subs):
		self.count = count
		self.fromt = fromt
		self.tot = tot
		self.subs = subs
		
	def delay(self, ms):
		self.fromt += datetime.timedelta(milliseconds=ms)
		self.tot += datetime.timedelta(milliseconds=ms)

	def __str__(self):
		sio = StringIO.StringIO()
		print >> sio, self.count
		
		fromt = datetime.datetime(1, 1, 1)
		tot = datetime.datetime(1, 1, 1)
		fromt += self.fromt
		tot += self.tot
		print >> sio, '%d:%d:%d,%d --> %d:%d:%d,%d' % (
			fromt.hour,
			fromt.minute,
			fromt.second,
			fromt.microsecond/1000,
			tot.hour,
			tot.minute,
			tot.second,
			tot.microsecond/1000
			)
			
		for sub in self.subs:
			print >> sio, sub
			
		return sio.getvalue()

def subtitles(f): #assume well-formatted
	data = False

	try:
		while True:
			count = int(f.next().strip())
			
			data = True

			fromto = f.next().strip()
			froms, tos = [x.strip() for x in fromto.split('-->')]
			h, m, etc = froms.split(':')
			s, ms = etc.split(',')
			h, m, s, ms = int(h), int(m), int(s), int(ms)
			fromt = datetime.timedelta(hours=h, minutes=m, seconds=s, milliseconds=ms)
			h, m, etc = tos.split(':')
			s, ms = etc.split(',')
			h, m, s, ms = int(h), int(m), int(s), int(ms)
			tot = datetime.timedelta(hours=h, minutes=m, seconds=s, milliseconds=ms)

			subs = []
			while True:
				subline = f.next().strip()
				if subline:
					subs.append(subline)
				else:
					break

			subtitle = Subtitle(count, fromt, tot, subs)
			yield subtitle
			
			data = False
	except StopIteration:
		if data:
			subtitle = Subtitle(count, fromt, tot, subs)
			yield subtitle
		return

def delaysubtitles(f, ms):
	for subtitle in subtitles(f):
		subtitle.delay(ms)
		print subtitle

if __name__ == '__main__':
	import optparse

	op = optparse.OptionParser()
	op.add_option('-f', '--file', dest='f', help='path to .srt file')
	op.add_option('-t', '--ms', type='int', dest='ms', help='delay in milliseconds')
	options, args = op.parse_args()

	f = open(options.f)
	delaysubtitles(f, options.ms)
	f.close()
