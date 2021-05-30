import sys; args = sys.argv[1:]
idx = int(args[0])-50


myRegexLst = [
  r"/\b\w*(\w)\w*\1\w*\b/i",
  r"/\w*(\w)(\w*\1){3}\w*/i",
  r"/^(0[01]*0|1[01]*1|[01])$/",
  r"/(?=\b\w{6}\b)\w*cat\w*/i",
  r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/ism",
  r"/\b((?!cat)\w){6}\b/i",
  r"/\b(?!\w*(\w)\w*\1)\w+/i",
  r"/^(?![01]*10011)[01]*$/",
  r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i",
  r"/^(1(?!01|11)|0)*$/"
   ]


if idx < len(myRegexLst):
  print(myRegexLst[idx])