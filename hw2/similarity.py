import sys
import time

# Define a function to preprocess data, generate list of movie and dictionaries of ratings and users for each movie
def preprocess_data(data):

    dataDict = {}
    userSet, mvSet = set(), set()
    n = len(data)

    # Generate dataDict[movie id][user id] = rating
    for i in range(n):
        user, mv, rating = data[i][0:3]
        userSet.add(user)
        mvSet.add(mv)

        if mv not in dataDict:
            dataDict[mv] = {}

        dataDict[mv][user] = int(rating)

    # Convert movie id and user id into int for sorting, then convert back to string for output
    userList = list(map(str, sorted(list(map(int, list(userSet))))))
    mvList = list(map(str, sorted(list(map(int, list(mvSet))))))

    return mvList, userList, dataDict

# Define a funticon to calculate the similarity of two movies
def similarity(mv1, mv2, dataDict, user_thresh):

    # Extract rating and user data of two movies from dictionaries, get the set of users rating for both movies
    data1, data2 = dataDict[mv1], dataDict[mv2]
    user1, user2 = set(data1.keys()), set(data2.keys())
    userCommon = user1 & user2
    # Set a default value less than -1 to represent the similarity in some special situations
    p = -10

    # When common user is not enough or calculating the same two movies, output similarity as p = -10
    if len(userCommon) >= user_thresh and mv1 != mv2:
        r1, r2 = [], []
        r1_all, r2_all = list(data1.values()), list(data2.values())

        for user in userCommon:
            r1.append(data1[user])
            r2.append(data2[user])

        # Calculate average of all ratings for each movie
        r1_avg, r2_avg = sum(r1_all) / len(r1_all), sum(r2_all) / len(r2_all)
        r1, r2 = [x - r1_avg for x in r1], [x - r2_avg for x in r2]
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
def similarityAll(mvList, dataDict, user_thresh):

    n = len(mvList)
    simList, commonList = [], []
 
    # Calculate similarity and number of common users for movie i and movie j (i > j), store them into List[i][j] and List[j][i]
    for i in range(n):
        simList.append([])
        commonList.append([])

        for j in range(i):
            simList[i].append(simList[j][i])
            commonList[i].append(commonList[j][i])

        for j in range(i, n):
            p, nCommon = similarity(mvList[i], mvList[j], dataDict, user_thresh)
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

        if simMax >= -1:
            mvMax = mvList[simList[i].index(simMax)]
            nCommon = commonList[i][simList[i].index(simMax)]
            result += ' (' + mvMax + ', ' + str('%.6f'%simMax) + ', ' +  str(nCommon) + ')'
            results.append(result)

    return results

# Define the main function of whole program
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
    mvList, userList, dataDict = preprocess_data(data)
    simList, commonList = similarityAll(mvList, dataDict, user_thresh)
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

#--style_0
#--Don't forget to insert line breaks to avoid long lines.
#--END

#--correctness_0
#--Good job!
#--END
