#include <iostream>
#include <thread>
#include <unistd.h>

class CThread{
	CThread():mThread(run, NULL){}
	CThread(void* argv):mThread(run, argv){}
	~CThread(){
		mThread.join();
	}

public:
	virtual void run(CThread *pThread, void *argv){
		this.argv = argv;
		std::cout << "CThread start running" << std::endl;
		int n = 0;
		while(n > 5){
			std::cout << "n = "  << n << std::endl;
			n++;
			sleep(1);
		}
	}
	virtual bool start();

private:
	void *argv;
	std::thread mThread;

};

int main()
{
	CThread mthd();
}
