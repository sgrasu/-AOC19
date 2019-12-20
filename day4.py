def adjacent(nums):
    counter = 1
    for i in range(len(nums)):
        if nums[i] == nums[i - 1]:
            counter += 1
        else:
            if counter == 2:
                return True
            counter = 1
    return counter == 2
    
minim = 246515
maxim = 739105

def findInRange(current = []):
    count = 0
    if len(current) >= 6:
        if adjacent(current) and minim <= int(''.join(map(str,current))) <= maxim:
            return 1
        return 0
    else:
        start = 2 if len(current) == 0 else current[-1]
        end = 8 if len(current) == 0 else 10
        for i in range(start,end):
            current.append(i)
            count += findInRange(current)
            current.pop()
    return count
print(findInRange())