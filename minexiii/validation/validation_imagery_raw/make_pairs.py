#!/usr/bin/env python

# This software was developed at the National Institute of Standards and
# Technology (NIST) by employees of the Federal Government in the course
# of their official duties. Pursuant to title 17 Section 105 of the
# United States Code, this software is not subject to copyright protection
# and is in the public domain. NIST assumes no responsibility whatsoever for
# its use by other parties, and makes no guarantees, expressed or implied,
# about its quality, reliability, or any other characteristic.

import random;
import os;

print "\tconst std::list<std::pair<std::string, std::string>> SAMPLE_PAIRS = {"

# [subject : [finger : (encounter1, encounter2, ...)]]
subjects = dict()

for filename in os.listdir('.'):
	try:
		subject, encounter, finger = filename.replace(".raw", ".raw.tmpl").split('_')
	except:
		continue

	# Skip "enrollment" template
	if encounter == "def":
		continue
		
	if not subject in subjects:
		subjects[subject] = dict()
	if not finger in subjects[subject]:
		subjects[subject][finger] = tuple()
	subjects[subject][finger] += (encounter,)
	
# Start with genuine encounter -> enrollment
for subject in subjects:
	for finger in subjects[subject]:
		for encounter in subjects[subject][finger]:
			print "\t\t{{\"{subject}_{encounter}_{finger}\", \"{subject}_def_{finger}\"}},".format(subject = subject, encounter = encounter, finger = finger)

# Add some genuine encounter -> encounter 
for subject in subjects:
	for finger in subjects[subject]:
		for i in range(0, 3):
			encounter1 = random.choice(subjects[subject][finger])
			encounter2 = random.choice(subjects[subject][finger])
			print "\t\t{{\"{subject}_{encounter1}_{finger}\", \"{subject}_{encounter2}_{finger}\"}},".format(subject = subject, encounter1 = encounter1, encounter2 = encounter2, finger = finger)

# Finish with impostors
subject_ids = subjects.keys()
num_impostor = 0
max_impostor = 1000
for i in range(0, max_impostor):
	subject1 = random.choice(subject_ids)
	subject2 = random.choice(subject_ids)
	if subject1 == subject2:
		continue
	
	fingers = subjects[subject1].keys()
	finger = random.choice(fingers)
	if finger not in subjects[subject2]:
		continue
	
	encounter1 = random.choice(subjects[subject1][finger])
	encounter2 = random.choice(subjects[subject2][finger])

	print "\t\t{{\"{subject1}_{encounter1}_{finger}\", \"{subject2}_{encounter2}_{finger}\"}}{comma}".format(subject1 = subject1, encounter1 = encounter1, subject2 = subject2, encounter2 = encounter2, finger = finger, comma = ("," if i != max_impostor - 1 else ""))
	num_impostor += 1

print "\t\t/* Num Impostor = {0} */".format(num_impostor)
print "\t};"

