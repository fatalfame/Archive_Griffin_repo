//
//  Pattern.m
//  Blink1Control
//
//  Created by Tod E. Kurt on 10/10/12.
//  Copyright (c) 2012 ThingM. All rights reserved.
//

#import "Blink1Pattern.h"

@implementation Blink1Pattern

@synthesize name;
@synthesize colors;
@synthesize times;
@synthesize repeats;
@synthesize playpos;
@synthesize playcount;
@synthesize playing;
@synthesize mode;
@synthesize blink1;


// parse color pattern text format
//
- (Boolean) setupFromPatternString:(NSString*)patternstr
{
    NSArray* parts = [patternstr componentsSeparatedByString:@","];
    
    repeats = [[parts objectAtIndex:0] intValue];
    playpos = 0;
    playcount = 0;
    colors = [NSMutableArray array];
    times  = [NSMutableArray array];
    playing = false;
    
    int len2x = (int)[parts count] - 1;
    if( (len2x % 2) == 0 ) {    // even number, so good
        for( int i=0; i<len2x; i+=2 ) {
            NSString* colorstr = [parts objectAtIndex:1+i+0];
            NSString* timestr  = [parts objectAtIndex:1+i+1];
            NSColor* color = [Blink1 colorFromHexRGB:colorstr];
            NSNumber* secs = [NSNumber numberWithFloat:[timestr floatValue]];
            if( color == nil ) color = [Blink1 colorFromInt:0]; // default to black
            [colors addObject: color];
            [times  addObject: secs];
        }
    }
    else {
        return false;
    }
    return true;
}

//
// patternstr format "name,repeats,color1,color1time,color2,c2time,..."
//
- (id)initWithPatternString:(NSString *)patternstr name:(NSString*)namestr
{
    self = [super init];
    name = [NSString stringWithString:namestr];

    if( ![self setupFromPatternString:patternstr] ) {
        self = nil;
    }
    
    return self;
}

//
- (void) play
{
    NSTimeInterval nextTime = [[times objectAtIndex:playpos] doubleValue];
    NSColor* color = [colors objectAtIndex:playpos];
    playpos = 0;
    playcount = 0;
    playing = true;
    DLog(@"%@ play p:%d c:%d %@ nextTime:%f",name,playpos,playcount,[Blink1 hexStringFromColor:color],nextTime);

    float fadeTime = nextTime/2;     // FIXME: time between colors != time to fade
    [blink1 fadeToRGB:color atTime:fadeTime];
    
    // schedule for next color
    timer = [NSTimer timerWithTimeInterval:nextTime target:self selector:@selector(update) userInfo:nil repeats:NO];
    [[NSRunLoop mainRunLoop] addTimer:timer forMode:NSDefaultRunLoopMode];
}

//
- (void) stop
{
    DLog(@"stop! %@",name);
    //[NSObject cancelPreviousPerformRequestsWithTarget:self selector:@selector(update) object:nil];
    //[[NSRunLoop mainRunLoop] cancelPerformSelector:@selector(update) target:self argument:nil];
    playing = false;
    [timer invalidate];
    timer = nil;
}

// called by the player periodically
- (void) update
{
    if( !playing ) return;
    Boolean scheduleNext = true;
    playpos++;
    if( playpos == [times count] ) {
        playpos = 0;
        if( repeats != 0 ) {  // infinite
            playcount++;
            if( playcount == repeats ) {
                scheduleNext = false;
            }
        }
    }
    
    if( scheduleNext ) {
        NSTimeInterval nextTime = [[times objectAtIndex:playpos] doubleValue];
        NSColor* color = [colors objectAtIndex:playpos];
        DLog(@"%@ updt p:%d c:%d %@ nextTime:%f",name,playpos,playcount,[Blink1 hexStringFromColor:color],nextTime);
        [blink1 fadeToRGB:color atTime:nextTime/2];
        timer = [NSTimer timerWithTimeInterval:nextTime target:self selector:@selector(update) userInfo:nil repeats:NO];
        [[NSRunLoop currentRunLoop] addTimer:timer forMode:NSRunLoopCommonModes];
    } else {
        playing = false;
    }
    
}

// render pattern back to a string format
- (NSString*)patternString
{
    NSMutableArray* pattern = [NSMutableArray array];
    [pattern addObject:[NSNumber numberWithInt:repeats]];
    for( int i=0; i< [colors count]; i++) {
        [pattern addObject:[Blink1 hexStringFromColor:[colors objectAtIndex:i]]];
        [pattern addObject:[[times  objectAtIndex:i] stringValue]];
    }
    NSString* patternstr = [pattern componentsJoinedByString:@","];
    return patternstr;
}

// objective-c's "toString"
- (NSString*) description
{
    return [NSString stringWithFormat:
            @"Blink1Pattern: name=%@, repeats=%d playpos=%d, playcount=%d",
            name,repeats,playpos,playcount];
}


// used by SBJson
- (NSDictionary*) proxyForJson
{
    NSColor* playedcolr = (playing) ? [colors objectAtIndex: playpos] : nil;

    return [NSDictionary dictionaryWithObjectsAndKeys:
            self.name, @"name",
            [self patternString], @"pattern",
            [NSNumber numberWithBool:playing], @"playing",
            [NSNumber numberWithInt:playpos], @"playpos",
            [NSNumber numberWithInt:playcount], @"playcount",
            [NSNumber numberWithInt:repeats], @"repeats",
            [Blink1 hexStringFromColor:playedcolr], @"playedColor",
            nil];
}

// for use with NSUserDefaults
- (void) encodeWithCoder:(NSCoder *)encoder
{
    //Encode properties, other class variables, etc
    [encoder encodeObject:self.name forKey:@"name"];
    [encoder encodeObject:[self patternString] forKey:@"pattern"];
}

// for use with NSUserDefaults
- (id) initWithCoder:(NSCoder *)decoder
{
    if((self = [super init])) {
        //decode properties, other class vars
        self.name = [decoder decodeObjectForKey:@"name"];
        NSString* patternstr = [decoder decodeObjectForKey:@"pattern"];
        [self setupFromPatternString:patternstr]; // note: discards return val
    }
    return self;
}

@end
