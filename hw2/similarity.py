import sys
import time

# Define a function to preprocess data, generate list of movie and dictionaries of ratings and users for each movie
def preprocess_data(data):

    dataDict, userDict = {}, {}
    n = len(data)
    mvSet = set()
    userSet = set()

    # Convert rating and movie id into integer, store movie id and user id into set
    for i in range(n):
        userSet.add(int(data[i][0]))
        mvSet.add(int(data[i][1]))
        data[i][2] = int(data[i][2])

    # Convert set into list for sorting
    mvList = list(mvSet)
    userList = list(userSet)
    mvList.sort()
    userList.sort()

    # Convert movie id into string for output
    # Generate dataDict[movie id][user id] = rating, userDict[movie id] = set of users rating on this movie 
    for i in range(len(mvList)):
        mv = str(mvList[i])
        mvList[i] = mv
        dataDict[mv] = {}
        userDict[mv] = set()

    # Put data into dictionaries
    for i in range(n):
        user = data[i][0]
        mv = data[i][1]
        userDict[mv].add(data[i][0])
        dataDict[mv][user] = data[i][2]

    return mvList, userList, dataDict, userDict

# Define a funticon to calculate the similarity of two movies
def similarity(mv1, mv2, dataDict, userDict, user_thresh):

    # Extract rating and user data of two movies from dictionaries, get the set of users rating for both movies
    data1, data2, user1, user2 = dataDict[mv1], dataDict[mv2], userDict[mv1], userDict[mv2]
    userCommon = user1 & user2
    # Set a parameter p less than -1 to represent the similarity in some special situations
    p = -10

    # When common user is not enough or calculating the same two movies, output similarity as p = -10
    if len(userCommon) >= user_thresh and mv1 != mv2:
        r1, r2, r1_all, r2_all = [], [], [], []

        for user in user1:
            r1_all.append(data1[user])

        for user in user2:
            r2_all.append(data2[user])

        for user in userCommon:
            r1.append(data1[user])
            r2.append(data2[user])

        # Calculate average of all ratings for each movie
        r1_avg = sum(r1_all) / len(r1_all)
        r2_avg = sum(r2_all) / len(r2_all)
        r1 = [x - r1_avg for x in r1]
        r2 = [x - r2_avg for x in r2]
        s1, s2, s3 = 0, 0, 0

        # Calculate similarity
        for i in range(len(userCommon)):
            s1 += r1[i]*r2[i]
            s2 += pow(r1[i], 2)
            s3 += pow(r2[i], 2)

        # When denominator of the formula is 0, output similarity as p = -10
        if s2*s3 > 0:
            p = s1/pow(s2*s3, 0.5)

    return p, len(userCommon)

# Define a function to calculate the similarity for all movie pairs
def similarityAll(mvList, dataDict, userDict, user_thresh):

    n = len(mvList)
    simList = []
    commonList = []

    # Calculate similarity and number of common user for movie i and movie j (i > j), store them into List[i][j] and List[j][i]
    for i in range(n):
        simList.append([])
        commonList.append([])

        for j in range(i):
            simList[i].append(simList[j][i])
            commonList[i].append(commonList[j][i])

        for j in range(i, n):
            p, nCommon = similarity(mvList[i], mvList[j], dataDict, userDict, user_thresh)
            simList[i].append(p)
            commonList[i].append(nCommon)

    return simList, commonList

# Define a function to generate output result
def output(mvList, simList, commonList):

    n = len(mvList)
    results = []

    # Find the largest similarity for each movie
    for i in range(n):
        mv = mvList[i]
        simMax = max(simList[i])
        result = mv

        if simMax > -1:
            mvMax = mvList[simList[i].index(simMax)]
            nCommon = commonList[i][simList[i].index(simMax)]
            result += ' (' + mvMax + ',' + str('%.4f'%simMax) + ',' +  str(nCommon) + ')'
            results.append(result)

    return results

def main():

    # Print useful message if no arguments given
    if len(sys.argv) < 3:
        print("Usage:")
        print("  $ python3 similarity.py <data_file> <output_file> [user_thresh] (default = 5)")
        sys.exit()

    # Extract arguments from sys.argv
    data_file = sys.argv[1]
    output_file = sys.argv[2]
    try:
        user_thresh = int(sys.argv[3])
    except:
        user_thresh = 5

    # Load data
    with open(data_file, 'r') as f:
        data = [x.strip().split() for x in f.readlines()]

    # Calculate similarities and output
    timeStart = time.time()
    mvList, userList, dataDict, userDict = preprocess_data(data)
    simList, commonList = similarityAll(mvList, dataDict, userDict, user_thresh)
    results = output(mvList, simList, commonList)
    timeEnd = time.time()

    # Write resultes into file
    with open(output_file, 'w') as f:
        for result in results:
            f.write(result+'\n')

    # Print summary
    print("Input MovieLens file: {}".format(data_file))
    print("Output file for similarity data: {}".format(output_file))
    print("Minimum number of common users: {}".format(user_thresh))
    print("Read {} lines with total of {} movies and {} users".format(len(data), len(mvList), len(userList)))
    print("Computed similarities in {} seconds".format(timeEnd-timeStart))

    return

main()
