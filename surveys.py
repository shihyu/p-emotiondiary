#coding: UTF-8

import pprint

surveys = {u'CES-D': {u'prompt': u'How have you felt this week?', u'answers':{0: u'Rarely or none of the time (Less than one day)', 1: u'Some or a little of the time (1-2 days)', 2: u'Occasionally or a moderate amount of time (3-4 days)', 3: u'Most or all of the time (5-7 days)'}, u'questions': {1: "I was bothered by things that usually don't bother me.", 2: "I did not feel like eating; my appetite was poor.", 3: "I felt that I could not shake off the blues, even with help from my family or friends.", 4: "I felt that I was just as good as other people.", 5: "I had trouble keeping my mind on what I was doing.", 6: "I felt depressed.", 7: "I felt that everything I did was an effort.", 8: "I felt hopeful about the future.", 9: "I thought my life had been a failure.", 10: "I felt fearful.", 11: "My sleep was restless.", 12: "I was happy.", 13: "I talked less than usual.", 14: "I felt lonely.", 15: "People were unfriendly.",16: "I enjoyed life.", 17: "I had crying spells.", 18: "I felt sad.", 19: "I felt that people dislike me.", 20: "I could not get u'going."}}, u'BDI': {u'prompt': "Please select statements that are suitable about you.", u'scoring': {u'0â9': u'indicates minimal depression', u'10â18': u'indicates mild depression', u'19â29': u'indicates moderate depression', u'30â63': u'indicates severe depression'}, u'questions': {1: {0: "I do not feel sad.â¨", 1: "I feel sad.", 2: "I am sad all the time and I can't snap out of it.", 3: "I am so sad and unhappy that I can't stand it."}, 2: {0: "I am not particularly discouraged about the future.â¨", 1: "I feel discouraged about the future.â¨", 2: "I feel I have nothing to look forward to.â¨", 3: "I feel the future is hopeless and that things cannot improve."}, 3: {0: "I do not feel like a failure.â¨", 1: "I feel I have failed more than the average person.â¨", 2: "As I look back on my life, all I can see is a lot of failures.", 3: "I feel I am a complete failure as a person."}, 4: {0: "I get as much satisfaction out of things as I used to.", 1: "I don't enjoy things the way I used to.", 2: "I don't get real satisfaction out of anything anymore.", 3: "I am dissatisfied or bored with everything."}, 5: {0: "I don't feel particularly guilty", 1: "I feel guilty a good part of the time.", 2: "I feel quite guilty most of the time.", 3: "I feel guilty all of the time."}, 6: {0: "I don't feel I am being punished.", 1: "I feel I may be punished.â¨", 2: "I expect to be punished.", 3: "I feel I am being punished."}, 7: {0: "I don't feel disappointed in myself.", 1: "I am disappointed in myself.â¨", 2: "I am disgusted with myself.â¨", 3: "I hate myself."}, 8: {0: "I don't feel I am any worse than anybody else.", 1: "I am critical of myself for my weaknesses or mistakes.", 2: "I blame myself all the time for my faults.â¨", 3: "I blame myself for everything bad that happens."}, 9: {0: "I don't have any thoughts of killing myself.", 1: "I have thoughts of killing myself, but I would not carry them out.", 2: "I would like to kill myself.", 3: "I would kill myself if I had the chance."}, 10: {0: "I don't cry any more than usual.", 1: "I cry more now than I used to.â¨", 2: "I cry all the time now.â¨", 3: "I used to be able to cry, but now I can't cry even though I want to."}, 11: {0: "I am no more irritated by things than I ever was.â¨", 1: "I am slightly more irritated now than usual.â¨", 2: "I am quite annoyed or irritated a good deal of the time.", 3: "I feel irritated all the time."}, 12: {0: "I have not lost interest in other people.", 1: "I am less interested in other people than I used to be.", 2: "I have lost most of my interest in other people.", 3: "I have lost all of my interest in other people."}, 13: {0: "I make decisions about as well as I ever could.", 1: "I put off making decisions more than I used to.â¨", 2: "I have greater difficulty in making decisions more than I used to.", 3: "I can't make decisions at all anymore."}, 14: {0: "I don't feel that I look any worse than I used to.", 1: "I am worried that I am looking old or unattractive.â¨", 2: "I feel there are permanent changes in my appearance that make me look unattractive.", 3: "I believe that I look ugly."}, 15: {0: "I can work about as well as before.", 1: "It takes an extra effort to get started at doing something.", 2: "I have to push myself very hard to do anything.â¨", 3: "I can't do any work at all."}, 16: {0: "I can sleep as well as usual.â¨", 1: "I don't sleep as well as I used to.", 2: "I wake up 1-2 hours earlier than usual and find it hard to get back to sleep.", 3: "I wake up several hours earlier than I used to and cannot get back to sleep."}, 17: {0: "I don't get more tired than usual.â¨", 1: "I get tired more easily than I used to.â¨", 2: "I get tired from doing almost anything.", 3: "I am too tired to do anything."}, 18: {0: "My appetite is no worse than usual.â¨", 1: "My appetite is not as good as it used to be.", 2: "My appetite is much worse now.â¨", 3: "I have no appetite at all anymore."}, 19: {0: "I haven't lost much weight, if any, lately.", 1: "I have lost more than five pounds.â¨", 2: "I have lost more than ten pounds.", 3: "I have lost more than fifteen pounds."}, 20: {0: "I am no more worried about my health than usual.", 1: "I am worried about physical problems like aches, pains, upset stomach, or constipation.", 2: "I am very worried about physical problems and it's hard to think of much else.", 3: "I am so worried about my physical problems that I cannot think of anything else."}, 21: {0: "I have not noticed any recent change in my interest in sex.", 1: "I am less interested in sex than I used to be.", 2: "I have almost no interest in sex.", 3: "I have lost interest in sex completely."}}}, u'PHQ-9': {u'prompt': u'Please answer the following questions considering your recent emotions.', u'questions': {1: u'Little interest or pleasure in doing things?', 2: u'Feeling down, depressed, or hopeless?', 3.'Trouble falling or staying asleep, or sleeping too much?', 4: u'Feeling tired or having little energy?', 5: u'Poor appetite or overeating?', 6: u'Feeling bad about yourselfâor that you are a failure or have let yourself or your family down?', 7: u'Trouble concentrating on things, such as reading the newspaper or watching television?', 8:  u'Moving or speaking so slowly that other people could have noticed? Or the oppositeâbeing so fidgety or restless that you have been moving around a lot more than usual?', 9: u'Thoughts that you would be better off dead or of hurting yourself in some way?'}, u'answers': {0: u'Not at all', 1: u'Several Days', 2: u'More than half the days', 3: u'Nearly everyday'}}}

pprint.pprint(surveys)