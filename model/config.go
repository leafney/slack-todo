/**
 * @Author:      leafney
 * @GitHub:      https://github.com/leafney
 * @Project:     slack-togo
 * @Date:        2023-09-28 08:29
 * @Description:
 */

package model

type Slack struct {
	ChannelID string `koanf:"channel_id"`
	BotToken  string `koanf:"bot_token"`
	UserToken string `koanf:"user_token"`
	UserID    string `koanf:"user_id"`
	Mysql     Mysql  `koanf:"mysql"`
	Redis     Redis  `koanf:"redis"`
}

type Mysql struct {
	Username    string `koanf:"username"`
	Password    string `koanf:"password"`
	Path        string `koanf:"path"`          // 数据库地址:端口号
	Dbname      string `koanf:"db_name"`       // 数据库名称
	Config      string `koanf:"config"`        // 数据库连接时的其他配置
	MaxIdleConn int    `koanf:"max_idle_conn"` // 最大空闲连接数
	MaxOpenConn int    `koanf:"max_open_conn"` // 最大并发连接数
}

type Redis struct {
	Addr     string `koanf:"addr"`     // redis服务地址:端口号
	Password string `koanf:"password"` // redis密码
	DB       int    `koanf:"db"`       // redis数据库
}
