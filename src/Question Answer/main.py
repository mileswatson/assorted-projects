list1 = []
question = input().upper()
question = question.split()
question_word = question[0]
question.remove(question_word)
print(question)
for x in range (0,len(question)):
  word = question[x]
  if x == 0:
    second_word = word
  else:
    if word == "YOU":
      question[x] = "I"
      second_word = "AM"
    elif word == "YOUR":
      question[x] = "MY"
    elif word == "I":
      question[x] = "YOU"
      second_word = "ARE"
    elif word == "MY":
      question[x] = "YOUR"
    list1.append(question[x])
list1.append(second_word)
answer = " ".join(list1)
if question_word == "WHEN":
  ending = " IN TWO MINUTES"
elif question_word == "WHAT":
  ending = " AN INFLATABLE SPHERE OF RUBBER"
elif question_word == "WHERE":
  ending = " ON PLANET MARS"
elif question_word == "IS" or question_word == "ARE" or question_word == "AM" or question_word == "WAS":
  print("OF COURSE NOT")
  exit()
elif question_word == "WHY":
  print("BECAUSE THAT IS THE WAY THINGS ARE")
  exit()
print(answer + ending)
    