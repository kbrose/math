class knuth_bendix:
	def __init__(self,relators,MAX_DEPTH):
		self.reductions = set()
		for rel in relators:
			p = rel[0]*rel[1]
			q = rel[2]*rel[3]
			self.add_red(p,q)
		self.update_reds()
		self.show_reds()
		#self.expand_reds()

	# add the reduction p -> q in sorted order (q < p)
	def add_red(self,p,q):
		if p == q:
			return
		assert(p != '')
		if q < p:
			self.reductions.add((p,q))
		else:
			self.reductions.add((q,p))

	# reduce the word "a" using ONLY given reduction "red"
	def reduce_given(self,a,red):
		# first, guarantee termination.
		assert(red[0] != red[1])
		assert(red[0] != '')
		while red[0] in a:
			idx = a.index(red[0])
			a = a[:idx] + red[1] + a[idx + len(red[0]):]
		return a

	# reduce the word "a" using all known rules.
	def reduce_all(self,a):
		for red in self.reductions:
			if red[0] == a:
				continue
			a = self.reduce_given(a,red)
		return a

	# replaces all current reductions with any other reductions possible.
	def update_reds(self):
		changes_made = True
		while changes_made:
			changes_made = False
			reductions_copy = self.reductions.copy()
			for red in reductions_copy:
				red1_reduced = self.reduce_all(red[1])
				red0_reduced = self.reduce_all(red[0])
				if red1_reduced != red[1] or red0_reduced != red[0]:
					changes_made = True
				self.reductions.remove(red)
				self.add_red(red0_reduced,red1_reduced)

	def show_reds(self):
		for red in self.reductions:
			print '"' + red[0] + '"' + ' -> ' + '"' + red[1] + '"'


relators = [['a',2,'',0],['b',5,'',0],['ab',3,'',0],['ab',6,'',0]]
a = knuth_bendix(relators,100)
