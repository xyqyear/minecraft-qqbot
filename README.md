## MC-QQbot

***this is solely a project for me to practice python and learn asyncio***

***don't use it, unless you want to use a piece of shit***

***the doc bellow is solely used to prevent me from forgetting things and make the repository looks better***

### doc

- commands should be like
    
        /command argument0 argument1 @server
        # or
        /command argument0 argument1 @serveraka
        
        # e.g.
        /whitelist add xyqyear @vanilla
        /ban xyqyear @v
        
        if there is no @ specification, then send to default server
        
- mc command modules
    
    first, you need to declare a tuple called permissions, and add permissions the 
    module might need to the tuple.
        
        permissions = ('ban', )
    
    then, get_command and parse_response function should be provided by the module
    
    get_command function receives *session: CommandSession* and *args: str*, 
    returns (*minecraft command: str*, *permission: str*)
    
    get_command function could be async or not async.
    
    ***the parameters used bellow may be changed in the future***
    
    parse_response function receives *permission: str* and *response: str*, 
    returns *response_parse: str*
    
    finally, in \_\_init__.py file in plugins.mc, the module you created should be 
    imported and added to commands: dict
