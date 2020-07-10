# Internationalization Testing  

&emsp; Since this is an open-source project under developing, our goal is to run multi-translation web automated acceptance testing without modifying the origin test script, for those who were also interested in this topic, we sincerely invite you to expand the project with us by sending us Pull Request.  
&emsp; If you are interested in making contributions to the project [Expansion of New Keyword Proxy](#expansion-of-new-keyword-proxy) will be an essential topic.   

## Outline  

* [Goal](#goal)  
* [File Structure](#file-structure)  
* [Robot Framework Listener](#robot-framework-listener)  
* [Usage of Warning in Report](#usage-of-warning-in-report)  
* [Remove Warning in Report](#remove-warning-in-report)  
* [Expansion of New Keyword Proxy](#expansion-of-new-keyword-proxy)  
* [Reference](#reference)  

## Goal  

&emsp; When a web that originally supports a single language expands into supporting multiple languages, the automated acceptance testing of the web should also be expanded.  
&emsp; **The goal of the project is to use JSON format multilingual web page translation files to complete the acceptance test of multi-language web pages without changing the existing Robot Framework test scripts.**  
&emsp; In this way, it won't be necessary to implement a corresponding automated acceptance test for all the expend multiple languages web.  

## File Structure  
* All Robot files should put under the RegressionTest folder.  
![](https://i.imgur.com/0zIjkoV.png)



* All Listener files should put under the listeners folder  
![](https://i.imgur.com/iehyQ8P.png)
  

* All Language files should put under the languageFiles folder, the folder/file name should contain locale.  
![](https://i.imgur.com/6loiU87.png)



## Robot Framework Listener  
Robot Framework Listener currently support version 2 and version 3, therefore it is necessary to add up `ROBOT_LISTENER_API_VERSION` as follows:  

![](https://i.imgur.com/4YX7OKD.png)  


 The variables of the listener will be set as follow:  
 `-d out -L debug --listener listeners/I18nListener.py:zh-TW`  
>  NOTE:  
>  The end argument `zh-TW` may be replaced by any locale that we expected to test.  
>  ex. `zh-CN`, `en-US`, etc.  
 
 (a) [RED](https://github.com/nokia/RED) IDE  
 
 1. Go to Preferences  
![](https://i.imgur.com/w7ifLAb.png)  


 2. Expand the Robot Framework->Launching->Default Launch Configurations to set the **Additional Robot Framework arguments** with the listener:  
 `-d out -L debug --listener listeners/I18nListener.py:zh-TW` 
 ![](https://i.imgur.com/4ACrZzI.png)



(b) Command line

1. Go to project root  
![](https://i.imgur.com/crScmMQ.png)  


2. Run following command  
```
set ROBOT_ARGS=-d out -L debug --listener listeners/I18nListener.py:zh-TW 
python -m robot -F robot %ROBOT_ARGS% .
```

## Usage of Warning in Report  

The warning notification will show while multi-translation happen as follow:  

(a) xpath contains the multi-translation word.  

The report shows `WARN` on top of the report for a keyword that xpath contain the multi-translation word.  
![](https://i.imgur.com/o5zS7in.jpg)


By clicking the top`WARN`, it will go to the keyword information.  
The `INFO` shows the translation result and the screenshot where xpath located  
![](https://i.imgur.com/xBqcfCn.png)  


(b) keyword argument contains the multi-translation word.  

The report shows `WARN` on top of the report for keyword argument contains the multi-translation word.  
![](https://i.imgur.com/ShyRRtC.jpg)


By clicking the top`WARN`, it will go to the keyword information.  
![](https://i.imgur.com/ArEBHhy.jpg)


## Remove Warning in Report  

To remove the multi-translation warning of a specific word, we need to modify the argument of the listener.  

The following is an example of removing the multi-translation warning of `Support`.  

1. Before removing, there is a multi-translation warning for `Support`.  
![](https://i.imgur.com/4CV1x4J.png)  



2. Add up `Support` at the end of the listener.  
`-d out -L debug --listener listeners/I18nListener.py:zh-TW:Support`  

3. By running the same keyword again, the multi-translation warning for `Support` will be removed. The notify of warning been remove will be shown under the keyword information.
![](https://i.imgur.com/sdnmkNU.png)


To remove more than one multi-translation warning word,  
just add `+` between each word in the listener.  
`-d out -L debug --listener listeners/I18nListener.py:zh-TW:Support+SecondWord+ThirdWord`  

If the argument is too long. You can use 
`-d out -L debug --listener listeners/I18nListener.py:zh-TW:Not_show_warning.txt` and put words in the file.

## Expansion of New Keyword Proxy  

&emsp; Proxy function act as an agent of keyword by identifying the argument of keyword, meaning keywords with the same argument proxy by the same Proxy function. Therefore, if there is a keyword with the type of argument can't be identified by any of the existing Proxy function, new keyword proxy function will be needed.  
&emsp; The project provides expansion of keyword proxy, the new keyword proxy required to implement Proxy interface defined by the project, and the new keyword proxy `.py` file required to locate under [proxyContainer](https://ssl-gitlab.csie.ntut.edu.tw/107598058/tcse2020/tree/master/listeners/proxyContainer) folder. There're some examples of keyword proxy under proxyContainer folder, for example, [ElementTextShouldBeProxy.py](https://ssl-gitlab.csie.ntut.edu.tw/107598058/tcse2020/blob/master/listeners/proxyContainer/ElementTextShouldBeProxy.py), [FindElementsProxy.py](https://ssl-gitlab.csie.ntut.edu.tw/107598058/tcse2020/blob/master/listeners/proxyContainer/FindElementsProxy.py), etc.  

![](https://i.imgur.com/8qtjDmV.png)  

## Reference  

Sample Web Page: Microsoft official website-https://www.microsoft.com/