import sys; args = sys.argv[1:]
idx = int(args[0])-40


myRegexLst = [
  r"/^[x.o]{64}$/i",
  r"/^[xo]*\.[xo]*$/i",
  r"/^(.*\.o*x+|.*\.|\..*|x+o*\..*)$/i",
  r"/^.(..)*$/s",
  r"/^(1([10]{2})*[10]|0([10]{2})*)$/",
  r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i",
  r"/^(0|10)*1*$/",
  r"/^[bc]*a[bc]*$|^[bc]+$/",
  r"/^([bc]*a[bc]*a[bc]*)+$|^[bc]+$/",
  r"/^\b(2[20]*)??(1[20]*1[20]*)*\b$/"
   ]


if idx < len(myRegexLst):
  print(myRegexLst[idx])