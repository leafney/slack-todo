/**
 * @Author:      leafney
 * @GitHub:      https://github.com/leafney
 * @Project:     slack-togo
 * @Date:        2023-09-28 08:28
 * @Description:
 */

package core

import (
	"fmt"
	"github.com/leafney/slack-togo/global"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"log"
	"os"
)

func Gorm() {
	mysqlAdmin := global.GConfig.Mysql

	dsn := fmt.Sprintf("%s:%s@tcp(%s)/%s?%s", mysqlAdmin.Username, mysqlAdmin.Password, mysqlAdmin.Path, mysqlAdmin.Dbname, mysqlAdmin.Config)

	if db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{}); err != nil {
		log.Printf("[MySQL] connect error %v", err)
		os.Exit(1)
	} else {
		// Ping
		sqlDB, err := db.DB()
		if err != nil {
			log.Printf("[MySQL] init error %v", err)
			os.Exit(1)
		}

		if err = sqlDB.Ping(); err != nil {
			//	err log
			log.Printf("[MySQL] ping error %v", err)
			os.Exit(1)
		}

		// 连接池配置
		sqlDB.SetMaxIdleConns(mysqlAdmin.MaxIdleConn)
		sqlDB.SetMaxOpenConns(mysqlAdmin.MaxOpenConn)

		global.GDB = db
		log.Println("[MySQL] load success")
	}
}
