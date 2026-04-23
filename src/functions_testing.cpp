
int testing_ideas ()
{
  std::unique_ptr<std::vector<double>> Thread1 = std::make_unique<std::vector<double>> ();

  for (unsigned i = 0; i < 10; i++) {
	Thread1 -> push_back(distrib(eng));
  }

  for (auto i : *Thread1) {
	std::cout<<"Our random vector contains "<<i<<std::endl;
  }

  auto p1 = box_muller (eng, distrib);
  
  std::printf("Our random values from two standard normal distributions are X = %F and Y = %F", p1.first, p1.second);

  Function* myfun = new Function ("e(x)", "ln(x)");
  std::cout<<myfun->test_inv(2.4)<<std::endl;

  
}
  
