# 查找xpath里字符

l1 = '''<li>
										
										
										
											<i class="icon icon-yellow-triangle" title="企业直招职位保证真实有效"><b>企</b></i>
										
										
										
									
									<div class="sojob-item-main clearfix">
										<div class="job-info">
											<h3 title="招聘大数据开发">
												<a href="https://www.liepin.com/job/1915279526.shtml" data-promid="imscid=R000000075&amp;ckid=9d690ea47ad84fa1&amp;headckid=9d690ea47ad84fa1&amp;pageNo=1&amp;pageIdx4&amp;totalIdx=44&amp;sup=1&amp;siTag=LGV-fc5u_67LtFjetF6ACg%7EfA9rXquZc5IkJpXC-Ycixw&amp;d_sfrom=search_prime&amp;d_ckId=0c11796a7086e6f160375c1161883246&amp;d_curPage=1&amp;d_pageSize=40&amp;d_headId=0c11796a7086e6f160375c1161883246&amp;d_posi=44" target="_blank" onclick="tlog=window.tlog||[];tlog.push('c:w_sojob_jobclick_9')">
													大数据开发 </a>
												
											</h3>
											<p class="condition clearfix" title="18-36万_广州-天河区_统招本科_2年以上">
												<span class="text-warning">18-36万</span>
												
													
														<a href="https://www.liepin.com/gz/zhaopin/" data-selector="data-url" class="area">广州-天河区</a>
													
													
												
												<span class="edu">统招本科</span>
												<span>2年以上</span>
											</p>
											<p class="time-info clearfix">
												<time title="2019年04月28日">2小时前</time>
												
													
														<span title="反馈时间以工作日为准，周末和假期时间不会计算在内">投递后：5个工作日内反馈</span>
													
												
											</p>
										</div>
										<div class="company-info nohover">
											<p class="company-name">
														
															
															
																<a title="公司广州寄锦教育科技有限公司" target="_blank" href="https://www.liepin.com/company/8311755/?subJobKind=0">广州寄锦教育科技有限公司</a>
															
														
											</p>
											<p class="field-financing">
												
													
													
														
														<span>
															
																
																	<a class="industry-link" href="/company/000-040/" onclick="return false;" target="_blank">互联网/移动互联网/电子商务</a>
																
																
																
															
														</span>
														
													
												
											</p>
											
											
												<p class="temptation clearfix">
													
														<span>五险一金</span>
													
														<span>岗位晋升</span>
													
														<span>全勤奖</span>
													
														<span>午餐补助</span>
													
														<span>绩效奖金</span>
													
														<span>定期体检</span>
													
														<span>年度旅游</span>
													
														<span>生育补贴</span>
													
														<span>子女福利</span>
													
														<span>发展空间大</span>
													
												</p>
											
											


										</div>
									</div></li>'''


l2='''<li>
										
										
										
											<i class="icon icon-yellow-triangle" title="企业直招职位保证真实有效"><b>企</b></i>
										
										
										
									
									<div class="sojob-item-main clearfix">
										<div class="job-info">
											<h3 title="招聘中级大数据工程师">
												<a href="https://www.liepin.com/job/1916799819.shtml" data-promid="imscid=R000000075&amp;ckid=9d690ea47ad84fa1&amp;headckid=9d690ea47ad84fa1&amp;pageNo=1&amp;pageIdx2&amp;totalIdx=42&amp;sup=1&amp;siTag=LGV-fc5u_67LtFjetF6ACg%7EfA9rXquZc5IkJpXC-Ycixw&amp;d_sfrom=search_prime&amp;d_ckId=0c11796a7086e6f160375c1161883246&amp;d_curPage=1&amp;d_pageSize=40&amp;d_headId=0c11796a7086e6f160375c1161883246&amp;d_posi=42" target="_blank" onclick="tlog=window.tlog||[];tlog.push('c:w_sojob_jobclick_9')">
													中级大数据工程师 </a>
												
											</h3>
											<p class="condition clearfix" title="14-21万_广州-番禺区_本科及以上_3年以上">
												<span class="text-warning">14-21万</span>
												
													
														<a href="https://www.liepin.com/gz/zhaopin/" data-selector="data-url" class="area">广州-番禺区</a>
													
													
												
												<span class="edu">本科及以上</span>
												<span>3年以上</span>
											</p>
											<p class="time-info clearfix">
												<time title="2019年04月28日">1小时前</time>
												
													
														<span title="反馈时间以工作日为准，周末和假期时间不会计算在内">投递后：10个工作日内反馈</span>
													
												
											</p>
										</div>
										<div class="company-info nohover">
											<p class="company-name">
														
															
															
																<a title="公司广东方纬科技有限公司" target="_blank" href="https://www.liepin.com/company/7952002/?subJobKind=0">广东方纬科技有限公司</a>
															
														
											</p>
											<p class="field-financing">
												
													
														<span>O2O/生活服务</span>
														
													
													
												
											</p>
											
											
												<p class="temptation clearfix">
													
														<span>股票期权</span>
													
														<span>定期体检</span>
													
														<span>年度旅游</span>
													
														<span>五险一金</span>
													
												</p>
											
											


										</div>
									</div></li>'''
from lxml import etree

# 要提取互联网/移动互联网/电子商务 这些公司产业
# l1,和l2有个有a标签,有个没有

e1 = etree.HTML(l1)
print(etree.tostring(e1))
# 对于在a标签里面的,这样是获取不了的
#rule='//div/div[2]/p[2]/span/text()'
rule='string(//div/div[2]/p[2]/span)'
test=e1.xpath(rule)
print(test)
