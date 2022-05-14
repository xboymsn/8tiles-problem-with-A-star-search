import random

"""
برای ساختن حالات رندوم برای تست
"""
def randomStart():
    state = []
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    i = 0
    while i < 9:
        num = random.choice(nums)
        nums.remove(num)
        state.append(num)
        i += 1
    return state

"""
برای نمایش دادن حالت پازل
"""
def Display(state):
    for i in range(0, 9, 3):
        print(f" {state[i]}    {state[i + 1]}    {state[i + 2]}")
        if (i % 3) == 0:
            print("")


"""
ساختمان داده ی درخت برای نگهداری پازل ها
"""
class Node:

    """تابع کانستراکتور نود با اتربیوت های پازل،عمق،و هزینه ی کلی و لیست فرزندان"""
    def __init__(self, puzz, g = 0):

        self.puzzle = puzz
        self.childPuzzleList = [] #قبل از پاپ کردن این ها تبدیل به فرزند میشوند
        self.g = g
        self.f = self.g + self.puzzle.cost
        self.SetNodeList()


    """
لیست پازل های فرزند را میسازد و در زمانی که گره والد از صف پاپ میشود تبدیل به گره میشوند و وارد صف میشوند   
    """
    def SetNodeList(self):
        puzz = self.puzzle
        match puzz.childCount:
            case 2:
                self.childPuzzleList.append(puzzle(puzz.childs[0]));self.childPuzzleList.append(puzzle(puzz.childs[1]))
            case 3:
                self.childPuzzleList.append(puzzle(puzz.childs[0]));self.childPuzzleList.append(puzzle(puzz.childs[1]));self.childPuzzleList.append(puzzle(puzz.childs[2]))
            case 4:
                self.childPuzzleList.append(puzzle(puzz.childs[0]));self.childPuzzleList.append(puzzle(puzz.childs[1]));self.childPuzzleList.append(puzzle(puzz.childs[2]));self.childPuzzleList.append(puzzle(puzz.childs[3]))


"""
صف اولویت و مرتب سازی
"""
class Queue :

    def __init__(self,queue = []):
        self.queue = queue


    def QueueAppend(self,node):
        queue = self.queue
        queue.append(node)

    """برای پاپ کردن به کار میرود اما قبل از آنکه اولین عنصر صف را بیرون کند فرزندان آن را تولید میکند و وارد صف میکند و سپس صف را مرتب میکند"""
    def QueuePop(self):
        queue = self.queue
        nodeList = []


        for child in queue[0].childPuzzleList:#convert puzzles to nodes
            new_node =Node(child,queue[0].g+1)
            # if queue.count(new_node)!=0:
            nodeList.append(new_node)

        for node in nodeList:
            self.QueueAppend(node)
        queue.pop(0)
        self.queue = self.QueuoSort()

    """بر اساس f=h+g صف را مرتب میکند"""
    def QueuoSort(self):
        queue = self.queue
        return sorted(queue,key= lambda x:x.f)


    """تابع آزمون هدف"""
    def GoalCheck(self):
        if self.queue[0].puzzle.cost !=0:
            return True
        else:
            return False



"""
در این کلاس حالت فعلی پازل و ظاهر و هزینه و فرزندان آن نگهداری می شود  
"""
class puzzle :

    """تابع کانستراکتور پازل با اتربیوت های استیت(نشان دهنده ی ظاهر و تربیت پازل)،هزینه و فرزندان پازل"""
    def __init__(self,  state):
        self.state = state
        if state != None:
            # self.cost = self.h3(state)
            self.cost = self.h2(state)
            # self.cost = self.h1(state)
            self.childs = self.ChildGenerator()
        else:
            self.cost = None
            self.childs = None

    """در این تابع فرزندان یک شی پازل تولید می شود و همچنین هزینه ی آن ها محاسبه میشود"""
    def ChildGenerator(self):
        state = self.state
        zero = state.index(0)
        switchList = self.Switcher(zero)#لیست حانه هایی که میتوان با 0 جا به جا کرد
        childsCount = len(switchList)#تعداد فرزندان
        childsList = self.ChildListGenerator(childsCount)#تولید لیست خالی برای وارد کردن فرزندان
        puzzleList = self.PuzzleListGenerator(childsCount)#لیستی از پازل های خالی برای تولید فرزند
        h_list = []#لیست هزینه ی فرزندان

        """کاشی صفر را با دیگر کاشی ها جا به جا میکند"""
        self.MoveZero(zero,childsCount,childsList,switchList)

        """با استفاده از لیست استیت های تولید شده پازل های فرزند را تولید میکند"""
        self.ListToPuzzle(childsCount,puzzleList,childsList)

        for child in childsList:
            # h_list.append(self.h3(child))
            h_list.append(self.h2(child))
            # h_list.append(self.h1(child))

        self.childCount = len(childsList)#مشخص کردن تعداد فرزندان


        return childsList


    """با استفاده از استیت های ذخیره شده در لیست پازل  میسازد"""
    def ListToPuzzle(self, childsCount, puzzleList, childsList):
        i = childsCount - 1
        while i >= 0:
            puzzleList[i].state = childsList[i]
            i -= 1


    """پازل خالی تولید میکند برای نگهداری فرزندان"""
    def PuzzleListGenerator(self, childCount):
            match childCount:
                case 2:
                    a = puzzle(None) ; b =puzzle(None) ; return a,b
                case 3:
                    a = puzzle(None) ; b =puzzle(None) ; c = puzzle(None) ; return a,b,c
                case 4:
                    a = puzzle(None) ; b =puzzle(None) ; c = puzzle(None) ; d = puzzle(None) ; return a,b,c,d


    """کاشی خالی را با کاشی های مجاور جابه جا میکند تا فرزند تولید شود"""
    def MoveZero(self,zero, childsCount, childsList, switchList):
        i = childsCount - 1
        while i >= 0:
            childsList[i][switchList[i]], childsList[i][zero] = childsList[i][zero], childsList[i][switchList[i]]
            i -= 1


    """لیست  تولید میکند برای نگهداری فرزندان"""
    def ChildListGenerator(self, childCount):
        state = self.state
        match childCount:
            case 2:
                child1 = state.copy(); child2 = state.copy(); return child1, child2
            case 3:
                child1 = state.copy(); child2 = state.copy(); child3 = state.copy(); return child1, child2, child3
            case 4:
                child1 = state.copy(); child2 = state.copy(); child3 = state.copy(); child4 = state.copy(); return child1, child2, child3, child4


    """با استفاده از ساختار مچ کیس که اخیرا به پایتون اضافه شده است تعداد حالاتی که پازل میتواند به آن تغییر حالت بدهد را مشخص میکند و لیست این حالات ممکن را بر میگرداند"""
    def Switcher(self, zero):
        match zero:
            case 0:
                return [1, 3]
            case 1:
                return [0, 2, 4]
            case 2:
                return [1, 5]
            case 3:
                return [0, 4, 6]
            case 4:
                return [1, 3, 5, 7]
            case 5:
                return [2, 4, 8]
            case 6:
                return [3, 7]
            case 7:
                return [4, 6, 8]
            case 8:
                return [5, 7]


    """تایع هیوریستیک اولی که در کلاس معرفی شد"""
    def h1(self, child):
        distance = 0
        # index distance
        i = 0
        while i < 9:
            distance += abs(child.index(i) - goal_1.index(i))
            i += 1
        return distance


    def h3(self,child):
        distance = 0
        i=0
        while i<9:
            if child.index(i)!=goal_1.index(i):
                distance+=1
            i+=1
        return distance


    """تابع هیوریستیک دومی که در کلاس معرفی شد که بر اساس پیمایش سطر و ستون طراحی شده است"""
    def h2(self , child):
        distance = 0
        i = 0
        while i < 9:
            child_column = child.index(i) % 3
            goal_column = goal_1.index(i) % 3

            child_row = int(child.index(i) / 3)
            goal_row = int(goal_1.index(i) / 3)

            distance += abs((child_column) - (goal_column)) + abs((child_row) - (goal_row))
            i += 1
        return distance


if __name__ == '__main__':
    goal_1 = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    #حالت های تست
    test = [1,2,3,4,5,6,7,8,0]
    test_0 = [6,8,7,3,2,1,0,5,4]
    test_1 = [2,8,3,4,1,6,0,5,7]
    test_2 = [5,2,7,4,1,3,8,6,0]
    test_3 = [2,3,0,1,7,5,4,6,8]

    a = puzzle(test_0)
    a.ChildGenerator()

    n = Node(a)

    q = Queue()
    q.QueueAppend(n)

    i = 0
    while q.GoalCheck():
        q.QueuePop()
        Display(q.queue[0].puzzle.state)
        i+=1
        print(f"depth: {q.queue[0].g}")
        print(f"iteration: {i}")
        print("\n")
    print("DONE")
    input()