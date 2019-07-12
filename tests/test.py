from traceback import format_exc
import sys
import datetime


class Test:
    def __init__(self):
        self.name = 'Unnamed Test'
        self.method = lambda: None


class TestRun:
    def __init__(self, test: Test):
        self.test = test
        self.completed = False
        self.return_value = None
        self.error = None

    def succeeded(self):
        return self.completed and not self.error

    def run(self):
        try:
            self.return_value = self.test.method()
        except:
            self.error = format_exc()

        self.completed = True


class TestList:
    def __init__(self, name='Unnamed Test List'):
        self.name = name
        self.tests = []

    def add_test_from_method(self, method, name=None):
        if name is None:
            name = method.__name__

        new_test = Test()
        new_test.method = method
        new_test.name = name

        self.add_test(new_test)
        return method

    test = add_test_from_method

    def add_test(self, test: Test):
        self.tests.append(test)

    def run(self, out=sys.stdout):
        print(
            datetime.datetime.now(),
            file=out
        )

        tests_succeeded = 0
        for test in self.tests:
            test_run = TestRun(test)
            test_run.run()

            if test_run.succeeded():
                result = 'succeeded'
                tests_succeeded += 1
            else:
                result = 'failed'

            print(
                self.name, '-', test.name, '-',
                result, 'with return value', test_run.return_value,
                file=out
            )

            if test_run.error:
                print(
                    test_run.error,
                    file=out
                )

        print(
            self.name, '-',
            tests_succeeded, 'out of', len(self.tests),
            'tests succeeded.',
            file=out
        )

        if tests_succeeded == len(self.tests):
            return True
        else:
            return False


if __name__ == '__main__':
    def main():
        all_tests = TestList()
        all_tests.name = 'All Tests'

        @all_tests.test
        def test_int():
            assert 1 == 1

        @all_tests.test
        def test_float():
            assert 2.0 == 2.0

        all_tests.run()

        # with open('test_results.txt', 'w') as file:
        #     all_tests.run(file)

    main()


