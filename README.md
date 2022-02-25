# overwatch

Shout out to Overwatch-api for existing, this rely's on the ow-api.
Check out the repo: https://github.com/alfg/overwatch-api

## Story time
This began as me wanting to make a small python library to wrap the "ow-api" api, essentially create a "Overwatch.PullProile(name)" function on this was it. 

However now I want to expand the library, but alot...

## Goals 
1. Create high-level 'Overwatch' object to easily call for stats from ow-api
      - Do so asyncronously
2. Create a "pulling service" to pull data at set intervals 
   - Any data pulled from "ow-api" is all current, there is no way to obtain historic data :(. So I will record my own historic data
3. Integrate Mongodb to save all this data, wrapping mongodb with a python object for easy use
   - This includes starting, stopping, checking the 'mongod' ( or maybe mongosh) service, as well as some pythonic wraps for querying data 
4. Integrate some data anaylsis/visualization with pandas 
   - Just now gettting to this one
5. The final piece of it all is to throw up the data and visualization on a website (Probably django/react) in a way that others on my local network can interact with the data!!

Extended/For Fun Goal: Create a CLI application to interact with the data too (yes mongo has this but I'm thinking BIGGGER: comparing stats, making graphs, so on so fourth). Everything with a GUI must have a terminal equivalent right?... :)


## Progress So Far 
I'm coding as I'm learning.

I chose some of these libraries because I DONT have as much experience with them, time to learn! SOO... I'm bouncing from section to section but here is a rough overview:

#### HighLevel Overwatch Object
-------------------------------
The 'Overwatch' object relies on 2 classes for making it's calls: ow_http and Request. Currently both *work* but I want to add more checking to them. 

#### Everything Mongodb
-------------------------------
The Mongodb object again *works*, the mongodb process can be starter, stopped, have it's stat checked, insert data, and fetch some data. However still alot of work need 

#### Everythin Data Analysis 
-----------------------------
There is a "standard dataFrame" set up. I debated for a looongtime on how to handle the data. I wanted to be able to fully utilize pandas sorting, and data churning abilities, so it took me away to decided how to include ALOT of data per frame (versus making smaller frames, i.e. one frame per hero).

The standard frame: "HeroDf" is now produced ( CreateHeroDf()), with data pulled directly from mongodb being passed to it. That's about it on the pandas side of things :) 

#### Pull Service, Constantly pulling...
----------------------------------------
SO, in the current set up the pull service is simpily a python script that runs continualy. This is not ideal, nor practical, I'm planning on throwing the pull service and db on a rasberry pi someday. So I that brings up the following:

#### Modularity plan 
--------------------
Pull service modular, mongodb modular? I have experience with docker so I'll start there and see where we go. 


#### Testing plan
-----------------
Some type of unit testing integration would be awesome too 






