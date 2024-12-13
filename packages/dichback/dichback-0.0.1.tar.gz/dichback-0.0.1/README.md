# 二分回溯算法
一种节省步数的，效率高的回溯算法。

## 回溯逻辑

回溯步骤比较复杂，直接看代码可能会好一点

- 定义逻辑和-逻辑函数单元：

    - **logic_unit**(self, **effective_list**: *list*) -> *bool*： 接收一个列表（有效数据集合）作为参数，遍历每一个元素，存在一个元素不符合定义的逻辑时就返回False,否则返回True

- 进入**dichotomy_backtracking_algorithm**(**effective_list**)方法:

    1. **调用逻辑和-逻辑函数单元**（传参：*effective_list*）：返回*true*或者*false*

    2. **第一次调用**：如果返回值为*True*，则直接退出（因为所有元素均符合定义逻辑），返回值为*False*，则将有效列表二分为两个子列表（*子列表1*,*子列表2*），将子列表1作为参数返回**步骤1**

    3. **非第一次调用**：如果返回值为*True*,那么该列表内的所有元素均符合定义逻辑，将该列表元素全部加入*yes_list*，这个时候回溯到它的父列表中的其他子列表中（由于二分法，一个父列表一般就两个子列表，也就是说每一个列表最多只有一个同父同级列表），如果其他子列表返回*False*,那么继续分割子列表，直到子列表长度小于等于*lm*（这一个值事实上会影响算法优化程度，因为这个值限制了子列表的**最小长度**，防止深度优先搜索过度深入造成浪费，也就是说当lm=有效列表长度//3-1的时候，理论上列表最多被分割4次），会把子列表元素逐个穷举，返回*True*，则加入yes_list，然后回溯，将它的同父同级列表作为参数返回**步骤1**

暂时还没有配图，所以可能不太好理解

## 下载和调用

```bash
pip install dichback
```

示例程序
```python
from dichback import AlgorithmSet

class Al(AlgorithmSet):
    LIST = [i for i in range(1, 100) if i%10 == 0]
    def __init__(self):
        super().__init__()

    def logic_unit(self, effective_list: list) -> bool:
        # LIST = [i for i in range(1, 100) if i%2 == 0]
        # 也就是2,4,6,8,10,12...98
        # 在1,2,3,4..99这个数据样本中LIST的离散程度非常大
        # 因为在这个逻辑单元中相当于True,False,True.False...
        for i in effective_list:
            if not i in self.LIST:
                return False
        return True

if __name__ == '__main__':
    a = Al()
    rep = a.dichotomy_backtracking_algorithm([i for i in range(1, 100)])
    print(a.chance)
    print(rep)
```

dichback中**AlgorithmSet**类继承的时候强制要求定义逻辑元:
`logic_unit(self, effective_list: list) -> bool`

同时提供*self.counts*属性，查看逻辑元调用次数